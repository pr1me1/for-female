from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.news.models import Post
from apps.user.serializers.account_model import UserProfileResponseSerializer


class PostModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'card', 'author',)
        read_only_fields = ('id', 'author',)
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'card': {'required': False},
        }

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get('exclude_fields', [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_author(self, obj):
        exclude_fields = ['is_staff', 'is_superuser', 'email', 'is_active']
        exclude_profile_fields = ['user', 'phone_number', 'bio', 'id']
        author_serializer = UserProfileResponseSerializer(
            obj.author,
            context={'exclude_profile_fields': exclude_profile_fields, 'exclude_fields': exclude_fields}
        )

        return author_serializer.data


class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True)

    def get_user(self):
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            raise ValidationError({"error": "User not found or not authenticated."})
        return user

    @transaction.atomic
    def create(self, validated_data):
        author = self.get_user()
        title = validated_data.get('title')
        description = validated_data.get('description')

        post = Post.objects.create(author=author, title=title, description=description)
        return post
