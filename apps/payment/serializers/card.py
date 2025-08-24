from rest_framework import serializers

from apps.courses.enums import ProductTypeChoices
from apps.payment.models import UserCard


class CardModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCard
        fields = (
            "id",
            "user__username",
            # 'card_token',
            "provider__name",
            "cardholder_name",
            "last_four_digits",
            "brand",
            "expire_month",
            "expire_year",
            "is_confirmed",
        )
        read_only_fields = (
            "id",
            "user__username",
            # 'card_token',
            "provider__name",
            "cardholder_name",
            "last_four_digits",
            "brand",
            "expire_month",
            "expire_year",
            "is_confirmed",
        )


class AddCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=16, required=True)
    exp_month = serializers.CharField(max_length=2, required=True)
    exp_year = serializers.CharField(max_length=2, required=True)


class ConfirmCardSerializer(serializers.Serializer):
    card_id = serializers.IntegerField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    card_name = serializers.CharField(max_length=255, required=False)


class DeleteCardSerializer(serializers.Serializer):
    card_id = serializers.CharField(required=True)


class CardReceiptCreateSerializer(serializers.Serializer):
    product_type = serializers.ChoiceField(
        choices=ProductTypeChoices.choices, required=True
    )
    product_id = serializers.IntegerField(required=True)
    card_token = serializers.CharField(required=True)


class CardReceiptConfirmSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(required=True)
    card_token = serializers.CharField(required=True)
