from asyncio import exceptions
from logging import exception
from pydoc_data.topics import topics
import jwt
from django.conf import settings

from rest_framework import authentication

from django.contrib.auth.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split(" ")

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms="HS256")

            user = User.objects.get(username=payload["username"])
            return (user, token)

        except jwt.DecodeError as identifier:
            raise exceptions.AuthenticationFailed("Your token is invalid,login")
        except jwt.ExpiredSignatureError as identifier:
            raise exceptions.AuthenticationFailed("Your token is expired,login")

        return super().authenticate(request)
