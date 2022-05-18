from rest_framework import routers
from .views import (ClientPurseAPI,
                    TransactionAPI,
                    QueueClientTransactionsAPI)

urlpatterns = []

router = routers.SimpleRouter()

router.register('client', ClientPurseAPI)
router.register('transaction', TransactionAPI)
router.register('queue', QueueClientTransactionsAPI)

urlpatterns += router.urls
