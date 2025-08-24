from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import Question, Submission
from apps.news.serializers.submissions import SubmissionCreateSerializer, SubmissionModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class SubmissionCreateAPIView(CreateAPIView):
    serializer_class = SubmissionCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context


class SubmissionListAPIView(ListAPIView):
    pagination_class = StandardResultsSetPagination
    serializer_class = SubmissionModelSerializer

    def get_queryset(self):
        question = get_object_or_404(Question, pk=self.kwargs.get("pk"))
        user = self.request.user
        return Submission.objects.filter(question=question, user=user)

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class SubmissionDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = SubmissionModelSerializer

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def get_object(self):
        return get_object_or_404(Submission, pk=self.kwargs["pk"])

