from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.serializers.account_model import UserProfileResponseSerializer
from apps.user.serializers.login import LoginSerializer


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        response_data = {
            "user": UserProfileResponseSerializer(
                user, context={"request": request}
            ).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(response_data, status=status.HTTP_200_OK)
