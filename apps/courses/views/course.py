from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.courses.models import Course
from apps.courses.serializers.course import CourseCreateSerializer, CourseModelSerializer
from apps.courses.services.filtersets import CourseFilterByCategory


class CreateCourseAPIView(CreateAPIView):
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CourseListAPIView(ListAPIView):
    serializer_class = CourseModelSerializer
    queryset = Course.objects.all()
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = (
        '^title',
        '=author__username',
        '^author__email',
        '=author__profile__first_name',
        '=author__profile__last_name',
    )
    filterset_class = CourseFilterByCategory
    permission_classes = [AllowAny]


class CourseSetCardAPIView(GenericAPIView):
    serializer_class = CourseModelSerializer
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, course_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            course = Course.objects.get(id=course_id)
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

        if course.cover and hasattr(course.cover, 'delete'):
            course.cover.delete(save=False)

        course.cover = card_file
        course.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CourseDetailAPIView(GenericAPIView):
    serializer_class = CourseModelSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def _get_object(self, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)

        return course

    def patch(self, request, course_id, *args, **kwargs):
        course = self._get_object(course_id)
        serializer = self.serializer_class(course, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request, course_id, *args, **kwargs):
        course = self._get_object(course_id)
        return Response(self.serializer_class(course).data, status=status.HTTP_200_OK)

    def delete(self, request, course_id, *args, **kwargs):
        course = self._get_object(course_id)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


_all_ = ['CreateCourseAPIView', 'CourseListAPIView', 'CourseSetCardAPIView']
