from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.payment.models import Transaction, Order
from apps.payment.serializers.transactions import TransactionModelSerializer


class TransactionListAPIView(ListAPIView):
    serializer_class = TransactionModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_orders = Order.objects.filter(user=self.request.user)
        return Transaction.objects.filter(order__in=user_orders)
