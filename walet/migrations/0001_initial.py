# Generated by Django 3.2.7 on 2021-09-30 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_account', models.CharField(max_length=60, verbose_name='Имя счета')),
                ('value_cash', models.PositiveIntegerField(verbose_name='Счет')),
                ('data_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cash_transaction', models.PositiveIntegerField(verbose_name='Сумма перевода')),
                ('data_at', models.DateTimeField(auto_now_add=True)),
                ('from_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_account', to='walet.cashaccount')),
                ('from_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='walet.cashaccount')),
                ('to_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
