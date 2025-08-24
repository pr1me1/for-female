from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from apps.courses.models import Lesson, Module
from apps.courses.serializers.module import ModuleModelSerializer


class LessonModelSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ("id", "title", "description", "file", "duration", "module")
        read_only_fields = ("id", "module")

    def get_module(self, obj):
        exclude_fields = ["course"]
        module_serializer = ModuleModelSerializer(
            obj.module,
            context={"exclude_fields": exclude_fields},
        )

        return module_serializer.data

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}


class LessonCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=128)
    duration = serializers.IntegerField()

    def get_user(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise PermissionDenied({"error": "User not found or not authenticated."})
        return user

    def check_permission(self, user, module):
        if user != module.course.author:
            raise PermissionDenied(
                "You are not authorized to add a module to this course."
            )

    @transaction.atomic
    def create(self, validated_data):
        user = self.get_user()
        module_id = self.context.get("module_id")

        try:
            module = Module.objects.get(id=module_id)
            self.check_permission(user, module)
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})

        lesson = Lesson.objects.create(
            title=validated_data.get("title"),
            description=validated_data.get("description"),
            duration=validated_data.get("duration"),
            module=module,
        )

        return LessonModelSerializer(lesson).data
