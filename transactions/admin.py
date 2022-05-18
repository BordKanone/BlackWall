from django.contrib import admin
from .models import ClientPurse, Transactions, QueueClientTransactions

admin.site.register(ClientPurse)
admin.site.register(Transactions)
admin.site.register(QueueClientTransactions)
