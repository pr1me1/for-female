import jwt
from django.conf import settings


def create_token(email, expires_in, user_pk):
    payload = {"email": email, "expires_in": expires_in, "user_pk": user_pk}

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
