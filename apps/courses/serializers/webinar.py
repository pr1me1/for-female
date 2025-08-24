from django.db import transaction
from rest_framework import serializers

from apps.courses.enums import FeeType
from apps.courses.models import Webinar, Category
from apps.courses.serializers.category import CategoryModelSerializer
from apps.user.serializers.account_model import UserProfileResponseSerializer


class WebinarModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Webinar
        fields = "__all__"
        extra_kwargs = {
            "title": {"required": False},
            "author_display_name": {"required": False},
            "description": {"required": False},
            "price": {"required": False},
            "cover": {"required": False},
            "category": {"required": False},
            "author": {"required": False, "null": True},
            "datetime": {"required": False},
            "status": {"required": False},
            "fee_type": {"required": False},
            "fee_amount": {"required": False},
        }
        read_only_fields = (
            "id",
            "author",
        )

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_author(self, obj):
        exclude_fields = [
            "is_staff",
            "is_superuser",
        ]
        exclude_profile_fields = ["last_name", "phone_number", "bio", "id"]
        author_serializer = UserProfileResponseSerializer(
            obj.author,
            context={
                "exclude_profile_fields": exclude_profile_fields,
                "exclude_fields": exclude_fields,
            },
        )

        return author_serializer.data

    def get_category(self, obj):
        exclude_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
        category_serializer = CategoryModelSerializer(
            obj.category, context={"exclude_fields": exclude_fields}
        )
        return category_serializer.data


class WebinarCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False, allow_blank=True)
    author_display_name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.CharField(required=False, allow_blank=True)
    datetime = serializers.CharField(required=False, allow_blank=True)
    fee_type = serializers.ChoiceField(
        choices=FeeType.choices, required=False, allow_blank=True
    )
    fee_amount = serializers.CharField(required=False, allow_blank=True)
    category_id = serializers.IntegerField(required=False)

    def get_user(self):
        user = self.context["request"].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"error": "User not authenticated."})
        return user

    @transaction.atomic
    def create(self, validated_data):
        user = self.get_user()
        category_id = validated_data.get("category_id")

        try:
            category = Category.objects.filter(id=category_id).first()
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        webinar = Webinar.objects.create(
            title=validated_data.get("title", ""),
            author_display_name=validated_data.get("author_display_name", ""),
            description=validated_data.get("description", ""),
            price=validated_data.get("price", "0"),
            datetime=validated_data.get("datetime", "0"),
            fee_type=validated_data.get("fee_type", "free"),
            fee_amount=validated_data.get("fee_amount", "0"),
            category=category,
            author=user,
        )
        webinar.save()

        return webinar
