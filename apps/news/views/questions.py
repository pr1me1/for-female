from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import Question, Survey
from apps.news.serializers.questions import QuestionCreateSerializer, QuestionModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class QuestionCreateAPIView(CreateAPIView):
    serializer_class = QuestionCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class QuestionListAPIView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = QuestionModelSerializer

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_queryset(self):
        survey_id = self.kwargs["pk"]
        try:
            survey= Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError("Event does not exist")

        return Question.objects.filter(survey=survey)

class QuestionDetailAPIView(RetrieveAPIView):
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_id = self.kwargs["pk"]
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return ValidationError("Question does not exist")

class QuestionUpdateAPIView(GenericAPIView):
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_id = self.kwargs["pk"]
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return ValidationError("Question does not exist")

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        question = self.get_object()
        if user != question.survey.author:
            raise PermissionDenied({"error": "Permission Denied"})
        serializer = self.get_serializer(question, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class QuestionDeleteAPIView(DestroyAPIView):
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_id = self.kwargs["pk"]
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return ValidationError("Question does not exist")

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        question = self.get_object()
        if user != question.survey.author:
            return PermissionDenied({"error": "Permission Denied"})
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionSetFileAPIView(GenericAPIView):
    serializer_class = QuestionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_id = self.kwargs["pk"]
        try:
            return Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            return ValidationError("Question does not exist")

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        question = self.get_object()
        if user != question.survey.author:
            raise PermissionDenied({"error": "Permission Denied"})

        file = request.FILES.get("file")
        if not file:
            return ValidationError("File does not exist")

        if file.size > 5 * 1024 * 1024:
            return Response(
                {
                    "detail": "Card file too big.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if question.file and hasattr(question.file, "delete"):
            question.file.delete(save=False)

        question.file = file
        question.save(update_fields=["file"])

        serializer = self.get_serializer(question)
        return Response(serializer.data)


_all_ = [
    'QuestionCreateAPIView',
    'QuestionListAPIView',
    'QuestionDetailAPIView',
    'QuestionUpdateAPIView',
    'QuestionDeleteAPIView',
    'QuestionSetFileAPIView',
]
