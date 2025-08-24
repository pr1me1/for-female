from django.db import transaction
from rest_framework import serializers

from apps.news.models import QuestionOption, Question
from apps.news.serializers.questions import QuestionModelSerializer


class QuestionOptionModelSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()

    class Meta:
        model = QuestionOption
        fields = (
            "id",
            "question",
            'title',
        )
        read_only_fields = ('id', 'question')


    def get_question(self, obj):
        if not obj.question:
            return None
        exclude_fields = ["survey"]
        question_serializer = QuestionModelSerializer(
            obj.question,
            context={
                **self.context,
                "exclude_fields": exclude_fields,
            },
        )

        return question_serializer.data

class QuestionOptionCreateSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    title = serializers.CharField()

    def get_question(self):
        question_id = self.validated_data.get("question_id")

        try:
            return Question.objects.get(pk=question_id)
        except Question.DeosNotExist:
            raise serializers.ValidationError({"detail": "Question does not exist"})

    @transaction.atomic
    def create(self, validated_data):
        question = self.get_question()

        title = validated_data.get("title", "")

        option = QuestionOption.objects.create(
            question=question,
            title=title,
        )

        return option
