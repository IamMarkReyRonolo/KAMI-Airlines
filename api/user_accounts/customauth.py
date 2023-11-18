import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from types import SimpleNamespace


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_data = authentication.get_authorization_header(request)

        if not auth_data:
            return None

        prefix, token = auth_data.decode("utf-8").split(" ")

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)
            payload["is_authenticated"] = True
            user = SimpleNamespace(**payload)
            return (user, token)
        except jwt.DecodeError as e:
            raise exceptions.AuthenticationFailed("Invalid Token")
        except jwt.ExpiredSignatureError as e:
            raise exceptions.AuthenticationFailed("Expired Token")
