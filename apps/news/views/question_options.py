from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    UpdateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import QuestionOption, Question
from apps.news.serializers.question_options import QuestionOptionCreateSerializer, QuestionOptionModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class QuestionOptionsCreateAPIView(CreateAPIView):
    serializer_class = QuestionOptionCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class QuestionOptionsRetrieveAPIView(RetrieveAPIView):
    serializer_class = QuestionOptionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_object(self):
        return get_object_or_404(QuestionOption, pk=self.kwargs["pk"])

class QuestionOptionsDestroyAPIView(DestroyAPIView):
    serializer_class = QuestionOptionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_option_id = self.kwargs["pk"]
        try:
            return QuestionOption.objects.get(id=question_option_id)
        except QuestionOption.DoesNotExist:
            raise ValidationError("Question option not found")

    def delete(self, request, *args, **kwargs):
        user = request.user
        question_option = self.get_object()
        if user != question_option.question.survey.author:
            raise PermissionDenied("You are not authorized to perform this action")
        question_option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class QuestionOptionsUpdateAPIView(UpdateAPIView):
    serializer_class = QuestionOptionModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        question_option_id = self.kwargs["pk"]
        try:
            return QuestionOption.objects.get(id=question_option_id)
        except QuestionOption.DoesNotExist:
            raise ValidationError("Question option not found")

    def patch(self, request, *args, **kwargs):
        question_option = self.get_object()
        if self.request.user != question_option.question.survey.author:
            raise PermissionDenied("You are not authorized to perform this action")
        serializer = self.get_serializer(question_option, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class QuestionOptionsListAPIView(ListAPIView):
    serializer_class = QuestionOptionModelSerializer
    pagination_class = StandardResultsSetPagination

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_queryset(self):
        question = get_object_or_404(Question, pk=self.kwargs.get("pk"))
        return question.options.all()
