from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField(required=True, allow_blank=False, allow_null=False)

    def validate_refresh(self, value):
        try:
            refresh_token = RefreshToken(value)
            return refresh_token
        except Exception as e:
            raise serializers.ValidationError({"refresh": "Invalid or expired refresh token."})

    def save(self):
        return self.validated_data["refresh"]
