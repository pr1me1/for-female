from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.courses.models import Module, Course
from apps.courses.serializers.course import CourseModelSerializer


class ModuleModelSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = "__all__"
        read_only_fields = ("course", "id")

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_course(self, obj):
        exclude_fields = [
            "id",
            "created_at",
            "updated_at",
            "author",
            "category",
            "description",
            "price",
            "discount",
            "card",
        ]
        category_serializer = CourseModelSerializer(
            obj.course, context={"exclude_fields": exclude_fields}
        )
        return category_serializer.data


class CreateModuleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=128)

    def get_user(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise ValidationError({"error": "User not found or not authenticated."})
        return user

    def get_course(self):
        course_id = self.context.get("course_id")
        if not course_id:
            raise ValidationError({"error": "Course ID is required."})

        try:
            return Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError({"error": "Course not found."})

    def check_permission(self, user, course):
        if user != course.author:
            raise PermissionDenied(
                "You are not authorized to add a module to this course."
            )

    def create(self, validated_data):
        user = self.get_user()
        course = self.get_course()
        self.check_permission(user, course)

        with transaction.atomic():
            return Module.objects.create(
                title=validated_data["title"],
                description=validated_data["description"],
                course=course,
            )
