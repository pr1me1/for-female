from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.courses.models import Webinar
from apps.courses.serializers.webinar import WebinarModelSerializer, WebinarCreateSerializer
from apps.courses.services.filtersets import CategoryFilter


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
        '^author__username',
        'author__email',
        '^author__profile__first_name',
        '^author__profile__last_name',
    )
    filter_class = CategoryFilter
    permission_classes = [AllowAny]


_all_ = ['WebinarCreateAPIView', 'WebinarListAPIView']
