from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.payment.models import Order
from apps.payment.serializers.order import OrderCreateSerializer, OrderModelSerializer


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderCreateSerializer
    permission_classes = [IsAuthenticated]


class DeleteOrderAPIView(DestroyAPIView):
    serializer_class = OrderModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_paid:
            return Response(
                {"error": "Order is already paid. And paid order cannot be deleted."}
            )

        self.perform_destroy(instance)
        return Response(
            {"message": "Order deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


_all_ = ["OrderCreateAPIView", "DeleteOrderAPIView"]
