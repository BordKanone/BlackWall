# Generated by Django 3.2 on 2022-05-17 21:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0002_auto_20220517_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientpurse',
            name='balance',
            field=models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Баланс'),
        ),
        migrations.AlterField(
            model_name='clientpurse',
            name='client',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='clientpurse',
            name='purse_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Номер кошелька'),
        ),
        migrations.AlterField(
            model_name='clientpurse',
            name='queue',
            field=models.ManyToManyField(blank=True, null=True, to='transactions.QueueClientTransactions', verbose_name='Очередь'),
        ),
        migrations.AlterField(
            model_name='queueclienttransactions',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Статус очереди'),
        ),
        migrations.AlterField(
            model_name='queueclienttransactions',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.clientpurse', verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='queueclienttransactions',
            name='transaction',
            field=models.ManyToManyField(blank=True, to='transactions.Transactions', verbose_name='Транзакция'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата и время'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='destination',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Получатель'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='queue',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='transactions.queueclienttransactions', verbose_name='Очередь'),
        ),
        migrations.AlterField(
            model_name='transactions',
            name='value',
            field=models.DecimalField(decimal_places=10, max_digits=19, verbose_name='Значение'),
        ),
    ]