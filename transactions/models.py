from django.db import models
from django.contrib.auth import get_user_model
from utils.constants import OPERATIONS


class ClientPurse(models.Model):
    name = models.CharField(max_length=128, verbose_name='Имя пользователя', blank=True, null=True)
    client = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE,
                                  related_name='client', verbose_name='Клиент', null=True, blank=True)
    purse_number = models.CharField(verbose_name='Номер кошелька', max_length=255, unique=True)
    balance = models.DecimalField(verbose_name='Баланс', max_digits=19, decimal_places=10)
    queue = models.ManyToManyField('QueueClientTransactions', blank=True, verbose_name='Очередь')

    def __str__(self):
        return f'{self.client} - {self.purse_number}'

    class Meta:
        verbose_name = 'Баланс пользователя'
        verbose_name_plural = "Баланс пользователя"


class QueueClientTransactions(models.Model):
    transaction = models.ManyToManyField('Transactions', blank=True, verbose_name='Транзакция')
    client = models.ForeignKey(ClientPurse, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Клиент')
    active = models.BooleanField(verbose_name='Статус очереди', default=True)

    def save(self, *args, **kwargs):
        target_client = ClientPurse.objects.filter(id=self.client.id).first()
        print(target_client)
        super().save(*args, **kwargs)
        target_client.queue.add(self)
        target_client.save()

    def __str__(self):
        return f'Queue {self.client}'

    class Meta:
        verbose_name = 'Очередь транзакций'
        verbose_name_plural = "Очереди транзакций"


class Transactions(models.Model):
    value = models.DecimalField(verbose_name='Значение', max_digits=19, decimal_places=10)
    date = models.DateTimeField(verbose_name='Дата и время', auto_now_add=True)
    operations = models.CharField(verbose_name='Тип операции', choices=OPERATIONS, max_length=5)
    destination = models.CharField(verbose_name='Получатель', max_length=255, blank=True, null=True)
    queue = models.ForeignKey(QueueClientTransactions, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Очередь')

    def save(self, *args, **kwargs):
        target_purse = ClientPurse.objects.filter(purse_number=self.destination).first()
        target_queue = QueueClientTransactions.objects.filter(
            client__purse_number=target_purse.purse_number).first()
        if self.operations == 'ADD':
            new_purse_value = target_purse.balance + self.value
            target_purse.balance = new_purse_value
            target_purse.save()
        else:
            new_purse_value = target_purse.balance - self.value
            if new_purse_value < 0:
                raise ValueError({'success': False, 'errorMessage': 'Недостаточно средств'})
            else:
                target_purse.balance = new_purse_value
                target_purse.save()
        super().save(*args, **kwargs)
        target_queue.transaction.add(self)
        target_queue.save()

    def __str__(self):
        return f'Транзакция {self.date}: {self.destination} {self.operations}'

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = "Транзакции"
