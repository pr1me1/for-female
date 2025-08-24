from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
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

from apps.courses.models import Course, Module
from apps.courses.serializers.module import (
    CreateModuleSerializer,
    ModuleModelSerializer,
)


class CreateModuleAPIView(CreateAPIView):
    serializer_class = CreateModuleSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["course_id"] = self.kwargs.get("course_id")
        return context


class ModuleListAPIView(ListAPIView):
    serializer_class = ModuleModelSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ("^title",)
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        course_id = self.kwargs.get("course_id")
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise ValidationError({"error": "Course not found."})

        queryset = Module.objects.filter(course=course)
        return queryset


class ModuleDetailAPIView(RetrieveAPIView):
    serializer_class = ModuleModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        module_id = self.kwargs.get("module_id")
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Module not found."})

        return module


class ModuleUpdateAPIView(GenericAPIView):
    serializer_class = ModuleModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        module_id = self.kwargs.get("module_id")
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Module not found."})

        return module

    def patch(self, request, *args, **kwargs):
        module = self.get_object()
        serializer = self.get_serializer(
            module,
            data=request.data,
            context=self.get_serializer_context(),
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ModuleDeleteAPIView(DestroyAPIView):
    serializer_class = ModuleModelSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        module_id = self.kwargs.get("module_id")
        try:
            module = Module.objects.get(id=module_id)
        except Module.DoesNotExist:
            raise ValidationError({"error": "Module not found."})

        return module

    def delete(self, request, *args, **kwargs):
        module = self.get_object()
        module.delete()
        return Response(
            {"message": "Module deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


_all_ = ["CreateModuleAPIView", "ModuleListAPIView"]
