from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from walet.models import Transaction
from walet.serializers import UserSerializer, AccountsSerializer, TransactionSerializer, TransactionCreateSerializer
from rest_framework.views import APIView


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class TransactionAddView(APIView):
    def get(self, request, **kwargs):
        print(kwargs)
        transaction = Transaction.objects.filter(from_user__username=kwargs['from_name'], to_user__username=kwargs['to_name'])
        print(transaction)



        serializer = TransactionSerializer(transaction, many=True)

        return Response(serializer.data)


    def post(self, request, **kwargs):
        print(kwargs)
        print(request.data, 'data')
        data = request.data
        data.update(from_account=1, to_account=2)

        serializer = TransactionCreateSerializer(data=request.data, many=True)

        return Response(serializer.data)
