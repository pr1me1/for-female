from rest_framework import serializers

from apps.user.actions import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False, allow_blank=False, allow_null=False)
    username = serializers.CharField(required=False, allow_blank=False, allow_null=False)
    password = serializers.CharField(write_only=True, required=True, allow_blank=False, allow_null=False)

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')

        if email and username:
            raise serializers.ValidationError("Email and username cannot be both specified")

        return attrs

    def save(self):
        email = self.validated_data.get('email')
        username = self.validated_data.get('username')

        if email:
            user = User.objects.get(email=email)
        else:
            user = User.objects.get(username=username)

        return user
