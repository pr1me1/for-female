from django.contrib.auth import get_user_model as gmu
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.user.models import UserProfile
from apps.user.serializers.account_model import UserResponseSerializer
from apps.user.serializers.validate_email import ValidateEmailSerializer
from apps.user.services.validate_token import validate_token


class ValidateEmailView(GenericAPIView):
    serializer_class = ValidateEmailSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get("token")
        if not token:
            return Response({"detail": "Token is missing"}, status=400)

        payload = validate_token(token=token)
        user_pk = payload['user_pk']
        user = gmu().objects.get(pk=user_pk)

        user.is_active = True
        user.save()

        UserProfile.objects.get_or_create(user=user)

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "detail": "Email successfully validated!",
                "user": UserResponseSerializer(user).data,
                "token": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            },
            status=200)


_all_ = ["ValidateEmailView"]
