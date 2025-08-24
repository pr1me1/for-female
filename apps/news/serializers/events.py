import datetime

from django.db import transaction
from rest_framework import serializers

from apps.news.models import Event
from apps.user.serializers.account_model import UserProfileResponseSerializer


class EventModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id',
            'title',
            'description',
            'author',
            'date',
            'location',
            'latitude',
            'longitude',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at', 'id', 'author')
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'date': {'required': False},
            'location': {'required': False},
            'latitude': {'required': False},
            'longitude': {'required': False},
        }

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_author(self, obj):
        if not obj.author:
            return {"author": None}
        exclude_fields = ["is_staff", "is_superuser", "email", "is_active"]
        exclude_profile_fields = ["user", "phone_number", "bio", "id"]
        author_serializer = UserProfileResponseSerializer(
            obj.author,
            context={
                "exclude_profile_fields": exclude_profile_fields,
                "exclude_fields": exclude_fields,
            },
        )

        return author_serializer.data

class EventCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)
    date = serializers.DateTimeField(required=False)

    def get_user(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"error": "User not found or not authenticated."})
        return user

    @transaction.atomic
    def create(self, validated_data):
        user = self.get_user()

        event = Event.objects.create(
            title=validated_data.get("title", ''),
            description = validated_data.get("description", ''),
            location = validated_data.get("location", ''),
            latitude = validated_data.get("latitude", 0.0),
            longitude = validated_data.get("longitude", 0.0),
            date = validated_data.get("date", datetime.datetime.now()),
            author = user
        )

        return event