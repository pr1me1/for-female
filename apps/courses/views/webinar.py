from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.courses.models import Webinar
from apps.courses.serializers.webinar import WebinarModelSerializer, WebinarCreateSerializer
from apps.courses.services.filtersets import WebinarFilterByCategory


class WebinarCreateAPIView(CreateAPIView):
    serializer_class = WebinarCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response = serializer.save()

        return Response(WebinarModelSerializer(response).data, status=status.HTTP_201_CREATED)


class WebinarListAPIView(ListAPIView):
    queryset = Webinar.objects.all()
    serializer_class = WebinarModelSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = (
        '^title',
        '=author__username',
        '^author__email',
        '=author__profile__first_name',
        '=author__profile__last_name',
    )
    filterset_class = WebinarFilterByCategory
    permission_classes = [AllowAny]


class WebinarSetCardAPIView(GenericAPIView):
    serializer_class = WebinarModelSerializer
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, webinar_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            webinar = Webinar.objects.get(id=webinar_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        card_file = request.FILES.get('card_file')
        if not card_file:
            return Response(
                {
                    "detail": "Card file not found.",
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if card_file.size > 5 * 1024 * 1024:
            return Response(
                {
                    "detail": "Card file too big.",
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if card_file.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
            return Response({
                "detail": f"Invalid file format. Allowed formats: {', '.join(['image/jpeg', 'image/png', 'image/gif'])}"}, )

        if webinar.cover and hasattr(webinar.cover, 'delete'):
            webinar.cover.delete(save=False)

        webinar.cover = card_file
        webinar.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class WebinarDetailAPIView(GenericAPIView):
    serializer_class = WebinarCreateSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def _get_object(self, webinar_id):
        try:
            course = Webinar.objects.get(id=webinar_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return course

    def patch(self, request, webinar_id, *args, **kwargs):
        webinar = self._get_object(webinar_id)
        serializer = self.serializer_class(webinar, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, webinar_id, *args, **kwargs):
        webinar = self._get_object(webinar_id)
        return Response(self.serializer_class(webinar).data, status=status.HTTP_200_OK)

    def delete(self, request, webinar_id, *args, **kwargs):
        webinar = self._get_object(webinar_id)
        webinar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


_all_ = ['WebinarCreateAPIView', 'WebinarListAPIView', 'WebinarSetCardAPIView', 'WebinarDetailAPIView']
