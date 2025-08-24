from django.db import transaction
from rest_framework import serializers

from apps.courses.models import Course
from apps.courses.serializers.course import CourseModelSerializer
from apps.news.models import Survey
from apps.user.serializers.account_model import UserProfileResponseSerializer


class SurveyModelSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()

    class Meta:
        model = Survey
        fields = (
            'id',
            'title',
            'description',
            'author',
            'created_at',
            'updated_at',
            'card',
            'course'
        )
        read_only_fields = ('created_at', 'updated_at', 'id', 'author')
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'card': {'required': False},
            'course': {'required': False},
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

    def get_course(self, obj):
        if not obj.course:
            return {"course": None}
        exclude_fields = ['author', 'description', 'created_at', 'updated_at', 'category']
        course_serializer = CourseModelSerializer(
            obj.course,
            context={
                "exclude_fields": exclude_fields,
            },
        )

        return course_serializer.data

class SurveyCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    course_id = serializers.IntegerField(required=True)

    def get_user(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"error": "User not found or not authenticated."})
        return user


    def get_course(self):
        course_id = self.validated_data.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError({"error": "Course not found"})

        return course

    @transaction.atomic
    def create(self, validated_data):
        user = self.get_user()
        course = self.get_course()

        survey = Survey.objects.create(
            title=validated_data.get("title", ''),
            description=validated_data.get("description", ''),
            course_id=validated_data.get("course_id"),
            author=user,
            course=course,
        )

        return survey


