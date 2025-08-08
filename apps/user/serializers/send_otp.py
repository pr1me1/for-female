from rest_framework import serializers


class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=32, min_length=8)

    def validate(self, attrs):
        email = attrs.get("email")

        if not email:
            raise serializers.ValidationError("Email is required.")
        return attrs

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 8:
            raise serializers.ValidationError("Password is too short.")
        if len(value) > 32:
            raise serializers.ValidationError("Password is too long.")
        return value
