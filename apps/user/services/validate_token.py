import time

from jwt import decode, InvalidTokenError
from rest_framework.exceptions import ValidationError

from core.settings.base import SECRET_KEY


def validate_token(token: str):
    try:
        payload = decode(token, SECRET_KEY, algorithms=["HS256"])
        expires_in = payload["expires_in"]
        if expires_in <= int(time.time()):
            raise ValidationError({"token": "Token is expired"})
    except InvalidTokenError:
        raise ValidationError("Invalid or expired token")

    return payload
