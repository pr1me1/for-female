import time

from jwt import decode, InvalidTokenError
from rest_framework.exceptions import ValidationError

from django.conf import settings

secret_key = settings.SECRET_KEY


def validate_token(token: str):
    try:
        payload = decode(token, secret_key, algorithms=["HS256"])
        expires_in = payload["expires_in"]
        if expires_in <= int(time.time()):
            raise ValidationError({"token": "Token is expired"})
    except InvalidTokenError:
        raise ValidationError("Invalid or expired token")

    return payload