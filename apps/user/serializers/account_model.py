from rest_framework import serializers

from apps.user.models import User, UserProfile


class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'email')


class ProfileResponseSerializer(serializers.ModelSerializer):
    # list_interests = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'avatar', "bio", "first_name", "last_name", "phone_number",)  # "list_interests"

    #
    # def get_list_interests(self, obj):
    #     return obj.list_interests.all()

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_profile_fields', [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}


class UserProfileResponseSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'profile')
        read_only_fields = ('id', 'is_active', 'is_staff', 'is_superuser', 'email')

    def get_profile(self, obj):
        exclude_profile_fields = self.context.get('exclude_profile_fields', [])
        profile_serializer = ProfileResponseSerializer(
            obj.profile,
            context={'exclude_profile_fields': exclude_profile_fields}
        )
        return profile_serializer.data

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_fields', [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}
