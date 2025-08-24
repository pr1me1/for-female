from django.db import transaction
from rest_framework import serializers

from apps.courses.models import Category, Course
from apps.courses.serializers.category import CategoryModelSerializer
from apps.user.serializers.account_model import UserProfileResponseSerializer


class CourseModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        read_only_fields = ("id", "author", "category")
        extra_kwargs = {
            "category": {"required": False, "write_only": True},
            "title": {"required": False},
            "description": {"required": False},
            "price": {"required": False},
            "discount": {"required": False},
            "author": {"required": False},
            "card": {"required": False},
        }

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

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

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


class CourseCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, allow_blank=False, allow_null=False)
    description = serializers.CharField(
        required=False, allow_blank=True, allow_null=True
    )
    category_id = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    def get_user(self):
        request = self.context.get("request")
        user = request.user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                {"error": "User was not found or not authenticated."}
            )

        return user

    @transaction.atomic
    def create(self, validated_data):
        user = self.get_user()
        category_id = validated_data.get("category_id")

        try:
            category = Category.objects.filter(id=category_id).first()
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        if not category:
            raise serializers.ValidationError({"category_id": "Invalid category"})

        course = Course.objects.create(
            title=validated_data["title"],
            description=validated_data.get("description", ""),
            category=category,
            author=user,
            price=validated_data["price"],
        )
        print(">>> Creating course", course)

        return course
