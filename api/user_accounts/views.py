from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from .models import KAMIUser
import jwt
from django.conf import settings


@swagger_auto_schema(method="POST", request_body=UserSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # encrypt password
        kami_user = KAMIUser.objects.get(username=serializer.data["username"])
        kami_user.set_password(serializer.data["username"])
        kami_user.save()

        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@swagger_auto_schema(method="POST", request_body=LoginSerializer)
@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        auth_token = jwt.encode(
            {
                "username": username,
                "id": user.id,
                "name": user.first_name + " " + user.last_name,
            },
            settings.JWT_SECRET_KEY,
        )
        serializer = UserSerializer(user)
        response_data = {
            "message": "Successfully logged in",
            "user": serializer.data,
            "access_token": str(auth_token),
        }
        return Response(response_data)
    else:
        return Response({"error": "Invalid credentials"}, status=400)
