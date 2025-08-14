from rest_framework import serializers

from apps.payment.paylov.constants import PaylovMethods


class PaylovSerializer(serializers.Serializer):
    id: serializers.IntegerField = serializers.IntegerField()
    method: serializers.ChoiceField = serializers.ChoiceField(
        choices=PaylovMethods.choices
    )
    params: serializers.JSONField = serializers.JSONField()
