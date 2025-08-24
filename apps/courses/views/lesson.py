from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    GenericAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.courses.models import Module, Lesson
from apps.courses.serializers.lesson import (
    LessonCreateSerializer,
    LessonModelSerializer,
)


class LessonCreateAPIView(CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["module_id"] = self.kwargs.get("module_id")
        return context


class LessonListAPIView(ListAPIView):
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        module_id = self.kwargs.get("module_id")
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        queryset = Lesson.objects.filter(module=module)
        return queryset


class LessonDetailAPIView(RetrieveAPIView):
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        lesson_id = self.kwargs.get("lesson_id")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Lesson not found."})

        return lesson


class LessonUpdateAPIView(GenericAPIView):
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        lesson_id = self.kwargs.get("lesson_id")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Lesson not found."})

        return lesson

    def patch(self, request, *args, **kwargs):
        lesson = self.get_object()
        serializer = self.get_serializer(
            lesson,
            data=request.data,
            context=self.get_serializer_context(),
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LessonDeleteAPIView(DestroyAPIView):
    serializer_class = LessonModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        lesson_id = self.kwargs.get("lesson_id")
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Lesson not found."})

        return lesson

    def delete(self, request, *args, **kwargs):
        lesson = self.get_object()
        lesson.delete()

        return Response(
            {"message": "Lesson haas been successfully deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


_all_ = [
    "LessonCreateAPIView",
    "LessonListAPIView",
    "LessonDetailAPIView",
    "LessonUpdateAPIView",
]
