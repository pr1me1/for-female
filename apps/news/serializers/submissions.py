from django.db import transaction
from rest_framework import serializers

from apps.news.models import Submission, Question, QuestionOption
from apps.news.serializers.questions import QuestionModelSerializer


class SubmissionModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()
    chosen_option = serializers.SerializerMethodField()
    text = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = (
            "id",
            "user",
            "question",
            "text",
            "chosen_option",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id",'created_at','updated_at', 'question')
        extra_kwargs = {
            'text': {'required': False},
            'chosen_option': {'required': False},
        }

    def get_user(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None

    def get_question(self, obj):
        if not obj.question:
            return None
        exclude_fields = [ "survey"]
        question_serializer = QuestionModelSerializer(
            obj.question,
            context={
                **self.context,
                "exclude_fields": exclude_fields,
            },
        )

        return question_serializer.data

    def get_chosen_option(self, obj):
        if not obj.chosen_option:
            return None
        exclude_fields = ["question"]
        question_serializer = QuestionModelSerializer(
            obj.chosen_option,
            context={
                exclude_fields: exclude_fields,
            }
        )

        return question_serializer.data

class SubmissionCreateSerializer(serializers.Serializer):
    chosen_option = serializers.IntegerField(required=False)
    text = serializers.CharField(required=False)
    question_id = serializers.IntegerField(required=True)

    def get_user(self):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({"error": "User not found or not authenticated."})
        return user

    def get_question(self):
        question_id = self.validated_data.get("question_id")

        try:
            return Question.objects.get(pk=question_id)
        except Question.DeosNotExist:
            raise serializers.ValidationError({"detail": "Question does not exist"})

    def get_option(self):
        chosen_option = self.validated_data.get("chosen_option")

        try:
            return QuestionOption.objects.get(pk=chosen_option)
        except QuestionOption.DoesNotExist:
            return None

    @transaction.atomic
    def create(self, validated_data):
        question = self.get_question()
        user = self.get_user()
        chosen_option = self.get_option()
        text = validated_data.get("text", "")

        submission = Submission.objects.create(
            user=user,
            question=question,
            text=text,
            chosen_option=chosen_option,
        )

        return submission


