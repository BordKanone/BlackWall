from rest_framework.viewsets import ModelViewSet
from .models import ClientPurse, QueueClientTransactions, Transactions
from .serializers import (TransactionSerializer,
                          QueueTransactionSerializer,
                          ClientPurseSerializer)


class ClientPurseAPI(ModelViewSet):
    queryset = ClientPurse.objects.all()
    serializer_class = ClientPurseSerializer


class TransactionAPI(ModelViewSet):
    queryset = Transactions.objects.all()
    serializer_class = TransactionSerializer


class QueueClientTransactionsAPI(ModelViewSet):
    queryset = QueueClientTransactions.objects.all()
    serializer_class = QueueTransactionSerializer

