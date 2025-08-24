from rest_framework import serializers
from django.db import transaction

from apps.news.enums import QuestionTypeChoices
from apps.news.models import Question, Survey
from apps.news.serializers.survey import SurveyModelSerializer


class QuestionModelSerializer(serializers.ModelSerializer):
    survey = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = (
            'id',
            'title',
            'type',
            'survey',
            'file',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')
        extra_kwargs = {
            'type': {'required': False},
            'title': {'required': False},
            "file": {"required": False},
            "survey": {"required": False},
        }

    def get_fields(self):
        fields = super().get_fields()
        exclude_fields = self.context.get("exclude_fields", [])
        return {k: v for k, v in fields.items() if k not in exclude_fields}

    def get_survey(self, obj):
        if not obj.survey:
            return None
        exclude_fields = ["id", "description", "author"]
        survey_serializer = SurveyModelSerializer(
            obj.survey,
            context={
                **self.context,
                "exclude_fields": exclude_fields,
            },
        )

        return survey_serializer.data

class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    type = serializers.ChoiceField(choices=QuestionTypeChoices.choices, required=True)
    survey_id = serializers.IntegerField(required=True)

    def get_survey(self):
        survey_id = self.validated_data.get("survey_id")
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            raise serializers.ValidationError({"error": "Survey not found"})

        return survey

    @transaction.atomic
    def create(self, validated_data):
        survey = self.get_survey()

        title = validated_data.get("title", "")
        type = validated_data.get("type", "")

        question = Question.objects.create(
            title=title,
            type=type,
            survey=survey,
        )

        return question

