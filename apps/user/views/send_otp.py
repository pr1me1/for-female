import time

from django.contrib.auth import get_user_model as gmu
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.user.serializers.send_otp import SendOTPSerializer
from apps.user.services.create_token import create_token
from apps.user.tasks.send_validation import send_validation_email


class SendOTPView(GenericAPIView):
    serializer_class = SendOTPSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        expires_in = int(time.time()) + 60 * 60 * 24 * 10

        user, _ = gmu().objects.get_or_create(
            email=email,
        )

        user.set_password(password)
        user.save(update_fields=['password'])

        if user.is_active:
            return Response({"message": "User already activated!"})

        if user.is_deleted:
            return Response({"message": "User has been deleted!"})

        token = create_token(email=email, expires_in=expires_in, user_pk=user.pk)

        send_validation_email(serializer.data['email'], token, request)
        return Response({"detail": "Validation email sent."}, status=200)


__all__ = ['SendOTPView']
