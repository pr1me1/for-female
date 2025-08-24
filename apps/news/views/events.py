from rest_framework import status
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.news.models import Event
from apps.news.serializers.events import EventCreateSerializer, EventModelSerializer
from apps.text_services.pagination import StandardResultsSetPagination


class EventCreateAPIView(CreateAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class EventUpdateAPIView(GenericAPIView):
    serializer_class = EventModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        event_id = self.kwargs["pk"]
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event does not exist")


    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

    def patch(self, request, *args, **kwargs):
        user = self.request.user
        event = self.get_object()
        if user != event.author:
            raise PermissionDenied({"error": "Permission Denied"})
        serializer = self.get_serializer(event, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EventListAPIView(ListAPIView):
    serializer_class = EventModelSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Event.objects.all()

    def get_serializer_context(self):
        exclude_fields = ("created_at", "updated_at", "description")
        context = super().get_serializer_context()
        context["exclude_fields"] = exclude_fields
        return context

class EventDetailAPIView(RetrieveAPIView):
    serializer_class = EventModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        event_id = self.kwargs["pk"]
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event does not exist")

class EventDeleteAPIView(DestroyAPIView):
    serializer_class = EventModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        event_id = self.kwargs["pk"]
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event does not exist")

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if request.user != event.author:
            raise PermissionDenied({"error": "Permission Denied"})
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventSetCardAPIView(GenericAPIView):
    serializer_class = EventModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        event_id = self.kwargs["pk"]
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            raise ValidationError("Event does not exist")

    def patch(self, request, pk, *args, **kwargs):
        event = self.get_object()

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

        if event.card and hasattr(event.card, "delete"):
            event.card.delete(save=False)

        event.card = card_file
        event.save(update_fields=["card"])

        serializer = self.get_serializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)






_all_ = ['EventCreateAPIView', 'EventUpdateAPIView', "EventListAPIView", "EventDetailAPIView", "EventDeleteAPIView", "EventSetCardAPIView"]

