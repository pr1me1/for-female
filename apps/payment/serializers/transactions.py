from rest_framework import serializers

from apps.payment.models import Transaction


class TransactionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'amount',
            'order',
            'status',
            'provider',
            'paid_at',
            'cancelled_at',
            'remote_id',
        )
        read_only_fields = (
            'id',
            'amount',
            'order',
            'status',
            'provider',
            'paid_at',
            'cancelled_at',
            'remote_id',
        )
