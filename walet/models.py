from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CashAccount(models.Model):
    name_account = models.CharField(max_length=60, verbose_name="Имя счета")
    value_cash = models.PositiveIntegerField(verbose_name="Счет")
    data_at = models.DateTimeField(auto_now_add=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}: {self.name_account}: {self.value_cash}"


class Transaction(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    from_account = models.ForeignKey(CashAccount, related_name='from_account', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE)
    to_account = models.ForeignKey(CashAccount, on_delete=models.CASCADE)
    cash_transaction = models.PositiveIntegerField(verbose_name="Сумма перевода")
    data_at = models.DateTimeField(auto_now_add=timezone.now)

    def __str__(self):
        return f"от {self.from_user} {self.from_account} сумма: {self.cash_transaction} кому: {self.to_user} {self.to_account}"