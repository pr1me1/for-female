from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user.models import User
from apps.user.serializers.account_model import UserProfileResponseSerializer
from apps.user.serializers.refresh import RefreshTokenSerializer


class RefreshTokenAPIView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.save()

        access_token = str(refresh_token.access_token)
        user_id = refresh_token.payload.get('user_id')
        try:
            user = User.objects.get(id=user_id, is_deleted=False)
        except User.DoesNotExist:
            raise serializers.ValidationError({"error": "User not found or has been deleted."})

        response_data = {
            "user": UserProfileResponseSerializer(user, context={'request': request}).data,
            "access": access_token
        }

        return Response(response_data, status=status.HTTP_200_OK)
