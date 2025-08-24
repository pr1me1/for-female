from django.db import transaction
from rest_framework import serializers

from apps.user.models import UserProfile, User


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ("first_name", "last_name", "phone_number", "bio")
        extra_kwargs = {
            "first_name": {"required": False, "allow_blank": True, "allow_null": False},
            "last_name": {"required": False, "allow_blank": True, "allow_null": False},
            "phone_number": {
                "required": False,
                "allow_blank": True,
                "allow_null": False,
            },
            "bio": {"required": False, "allow_blank": True, "allow_null": False},
        }

    def validate_phone_number(self, value):
        if value == "":
            return value  # Allow blank phone numbers
        return value


class ProfilePatchSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=64, required=False, allow_blank=True, allow_null=False
    )
    first_name = serializers.CharField(
        max_length=64, required=False, allow_blank=True, allow_null=False
    )
    last_name = serializers.CharField(
        max_length=64, required=False, allow_blank=True, allow_null=False
    )
    phone_number = serializers.CharField(
        max_length=64, required=False, allow_blank=True, allow_null=False
    )
    bio = serializers.CharField(
        max_length=128, required=False, allow_blank=True, allow_null=False
    )

    def validate_username(self, value):
        user = User.objects.filter(username=value).first()
        if not user and user != self._get_user():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def _get_user(self):
        request = self.context.get("request")
        user = request.user
        if not user:
            raise serializers.ValidationError({"error": "User was not found."})

        return user

    @transaction.atomic
    def save(self):
        validated_data = self.validated_data
        user = self._get_user()
        first_name = validated_data.get("first_name")
        last_name = validated_data.get("last_name")
        phone_number = validated_data.get("phone_number")
        bio = validated_data.get("bio")

        if "username" in validated_data:
            username = validated_data.get("username")
            user.username = username if username is not None else ""
            user.save()

        profile, _ = UserProfile.objects.get_or_create(
            user=user,
        )
        profile.last_name = last_name
        profile.first_name = first_name
        profile.phone_number = phone_number
        profile.bio = bio
        profile.save()

        return user
