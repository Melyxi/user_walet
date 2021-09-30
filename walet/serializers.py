from rest_framework.serializers import HyperlinkedModelSerializer
from .models import *
from rest_framework import serializers


class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashAccount
        fields = ('id', 'name_account', 'value_cash', 'data_at')


class UserSerializer(serializers.ModelSerializer):
    account_cash = AccountsSerializer(source='cashaccount_set', many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'date_joined', 'account_cash')


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TransactionCreateSerializer(serializers.ModelSerializer):
    from_account = AccountsSerializer()
    to_account = AccountsSerializer()
    class Meta:
        model = Transaction
        fields = ('from_account', 'to_account', 'cash_transaction')


class GetTransactionSerializer(serializers.Serializer):

    from_name = UserSerializer()
    to_name = UserSerializer()
    # from_user_accounts = AccountsSerializer(source='cashaccount_set', many=True)
    # to_user_accounts = AccountsSerializer(source='cashaccount_set', many=True)
