from django.db import transaction
from django.http.response import Http404
from rest_framework import permissions
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from apps.text_services.pagination import StandardResultsSetPagination
from apps.user.models import User, UserProfile
from apps.user.serializers.account_model import UserProfileResponseSerializer
from apps.user.serializers.profile import ProfilePatchSerializer


class ProfileModelAPIView(GenericAPIView):
    serializer_class = ProfilePatchSerializer

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        response = serializer.save()
        return Response(UserProfileResponseSerializer(response).data, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = UserProfileResponseSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = request.user
        with transaction.atomic():
            user.soft_delete()
        return Response(
            UserProfileResponseSerializer(user, context={'request': request}).data,
            status=status.HTTP_200_OK
        )


class ProfileDetailAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserProfileResponseSerializer

    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
        except User.DoesNotExist:
            raise Http404("User not found or has been deleted.")

        exclude_fields = ['is_staff', 'is_superuser', "is_active"]

        serializer = UserProfileResponseSerializer(user, context={'request': request, 'exclude_fields': exclude_fields})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileListAPIView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    serializer_class = UserProfileResponseSerializer
    authentication_classes = []
    filter_backends = (SearchFilter,)
    search_fields = ['username', 'email']
    queryset = User.objects.filter(is_deleted=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['exclude_fields'] = ['is_staff', 'is_superuser', ]
        context['exclude_profile_fields'] = ['last_name', 'phone_number', 'bio']
        return context


class ProfileAvatarSetAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileResponseSerializer

    def patch(self, request, *args, **kwargs):
        user = request.user

        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            return Response(
                {"detail": "No avatar file provided."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if avatar_file.size > 5 * 1024 * 1024:  # Limit to 5MB
            return Response(
                {"detail": "Avatar file size exceeds 5MB limit."},
                status=status.HTTP_400_BAD_REQUEST
            )

        allowed_formats = ['image/jpeg', 'image/png', 'image/gif']
        if avatar_file.content_type not in allowed_formats:
            return Response(
                {"detail": f"Invalid file format. Allowed formats: {', '.join(allowed_formats)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if profile.avatar and hasattr(profile.avatar, 'delete'):
            profile.avatar.delete(save=False)

        profile.avatar = avatar_file
        profile.save()

        serializer = self.get_serializer(user, context={
            'request': request,
            'exclude_fields': ['is_staff', 'is_superuser'],
        })
        return Response(serializer.data, status=status.HTTP_200_OK)


_all__ = ['ProfileModelAPIView', 'ProfileDetailAPIView', 'ProfileListAPIView', 'ProfileAvatarSetAPIView']
