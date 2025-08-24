from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import Survey
from apps.news.serializers.survey import SurveyCreateSerializer, SurveyModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class SurveyCreateAPIView(CreateAPIView):
    serializer_class = SurveyCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class SurveyListAPIView(ListAPIView):
    serializer_class = SurveyModelSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Survey.objects.all()

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at", "description")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class SurveyDetailAPIView(RetrieveAPIView):
    serializer_class = SurveyModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        survey_id = self.kwargs["pk"]
        try:
            return Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError("Survey does not exist")

class SurveyUpdateAPIView(GenericAPIView):
    serializer_class = SurveyModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        survey_id = self.kwargs["pk"]
        try:
            return Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError("Survey does not exist")

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context


    def patch(self, request, *args, **kwargs):
        user = self.request.user
        survey = self.get_object()
        if user != survey.author:
            raise PermissionDenied({"error": "Permission Denied"})
        serializer = self.get_serializer(survey, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SurveyDeleteAPIView(DestroyAPIView):
    serializer_class = SurveyModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        survey_id = self.kwargs["pk"]
        try:
            return Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError("Survey does not exist")

    def destroy(self, request, *args, **kwargs):
        survey = self.get_object()
        if request.user != survey.author:
            raise PermissionDenied({"error": "Permission Denied"})
        survey.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SurveySetCardAPIView(GenericAPIView):
    serializer_class = SurveyModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        survey_id = self.kwargs["pk"]
        try:
            return Survey.objects.get(pk=survey_id)
        except Survey.DoesNotExist:
            raise ValidationError("Event does not exist")

    def patch(self, request, pk, *args, **kwargs):
        survey = self.get_object()

        card_file = request.FILES.get("card_file")
        if not card_file:
            return Response(
                {
                    "detail": "Card file not found.",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if card_file.size > 5 * 1024 * 1024:
            return Response(
                {
                    "detail": "Card file too big.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if card_file.content_type not in ["image/jpeg", "image/png", "image/gif"]:
            return Response(
                {
                    "detail": f"Invalid file format. Allowed formats: {', '.join(['image/jpeg', 'image/png', 'image/gif'])}"
                },
            )

        if survey.card and hasattr(survey.card, "delete"):
            survey.card.delete(save=False)

        survey.card = card_file
        survey.save(update_fields=["card"])

        serializer = self.get_serializer(survey)
        return Response(serializer.data, status=status.HTTP_200_OK)


_all_=[
    'SurveyDetailAPIView',
    'SurveyUpdateAPIView',
    'SurveyDeleteAPIView',
    'SurveySetCardAPIView',
    'SurveyCreateAPIView',
    'SurveyListAPIView',
]
