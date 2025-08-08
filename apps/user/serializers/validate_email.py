from rest_framework import serializers


class ValidateEmailSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)
