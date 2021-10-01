from copy import copy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.contrib import auth
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db import transaction as transaction_db
from walet.models import Transaction, CashAccount
from walet.serializers import UserSerializer, AccountsSerializer, TransactionSerializer, TransactionCreateSerializer, \
    GetTransactionSerializer
from rest_framework.views import APIView


@login_required(login_url='/login/')
def main(request):
    return render(request, 'walet/main.html')


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = 'walet/login.html'
    success_url = reverse_lazy('main')


@login_required(login_url='/login/')
def profileview(request, pk=None):
    return render(request, 'walet/profile.html')


@login_required(login_url='/login/')
def cashaccount(request, pk=None):
    return render(request, 'walet/cashaccount.html')


@login_required(login_url='/login/')
def transaction(request, pk=None):
    return render(request, 'walet/transaction.html')


@login_required(login_url='/login/')
def transfer(request, name=None):
    return render(request, 'walet/transfer.html')


class AccountsViewSet(ModelViewSet):
    queryset = CashAccount.objects.all()
    serializer_class = AccountsSerializer


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserTransactionView(APIView, LimitOffsetPagination):
    def get(self, request, **kwargs):
        from_user = Transaction.objects.filter(Q(from_user__id=kwargs['user']) | Q(to_user__id=kwargs['user']))
        results = self.paginate_queryset(from_user, request, view=self)
        serializer = TransactionSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)


class TransactionAddView(APIView):
    def get(self, request, **kwargs):

        from_user = User.objects.filter(username=kwargs['from_name']).first()
        to_user = User.objects.filter(username=kwargs['to_name']).first()
        from_user_data = UserSerializer(from_user)
        to_user_data = UserSerializer(to_user)
        data = {'from_name': from_user_data.data, 'to_name': to_user_data.data}
        transaction = GetTransactionSerializer(data=data)

        transaction.is_valid()

        return Response(transaction.data)

    @transaction_db.atomic
    def post(self, request, **kwargs):
        data = request.data

        cash_transaction = data['cash_transaction']

        walets = data['from_account']
        print(walets)
        summ_balance = 0
        for walet in walets:
            from_walet = CashAccount.objects.filter(name_account=walet).first()
            balance = from_walet.value_cash
            summ_balance += balance
        if summ_balance < cash_transaction:
            return Response({'error': 'Недостаточно средств для перевода'})

        balance_walet = {}

        for walet in walets:
            walet_balance = CashAccount.objects.filter(name_account=walet).first()
            if walet_balance:
                cash = walet_balance.value_cash
                balance_walet[walet] = cash

        old_balance = copy(balance_walet)

        def len_dict(balance):
            len_dict = 0
            for bal in balance.items():
                if bal[1] > 0:
                    len_dict += 1
            return len_dict

        even_balance = cash_transaction / len_dict(balance_walet)

        while cash_transaction > 0:
            for itm in balance_walet.items():
                if itm[1] >= even_balance:
                    balance_walet[itm[0]] = itm[1] - even_balance
                    cash_transaction = cash_transaction - even_balance
                if itm[1] < even_balance:
                    balance_walet[itm[0]] = 0
                    cash_transaction = cash_transaction - itm[1]
            even_balance = cash_transaction / len_dict(balance_walet)

        from_user = User.objects.filter(username=kwargs['from_name']).first()
        to_user = User.objects.filter(username=kwargs['to_name']).first()

        data_res = []
        for i in balance_walet:
            cash = old_balance[i] - balance_walet[i]
            if old_balance[i] != 0:
                from_walet = CashAccount.objects.filter(name_account=i).first()
                to_walet = CashAccount.objects.filter(name_account=data['to_account']).first()

                from_walet.value_cash = balance_walet[i]
                from_walet.save()

                to_walet.value_cash += cash
                to_walet.save()

                transaction = Transaction(from_user=from_user, to_user=to_user, cash_transaction=cash,
                                          from_account=from_walet, to_account=to_walet)
                transaction.save()

                data_from = AccountsSerializer(from_walet)
                data_to = AccountsSerializer(to_walet)

                data_dict = dict(from_user=from_user, to_user=to_user, cash_transaction=cash,
                                 from_account=data_from.data, to_account=data_to.data)

                serialiser = TransactionCreateSerializer(data=data_dict)

                if serialiser.is_valid():
                    data_r = serialiser.data
                    data_res.append(data_r)
                else:
                    data_res.append(serialiser.errors)

        return Response(data_res)
