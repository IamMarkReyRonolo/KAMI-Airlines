from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework import status
from .models import Airplane
from .serializers import AirplaneSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from api.user_accounts.customauth import JWTAuthentication


@swagger_auto_schema(method="POST", request_body=AirplaneSerializer)
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def add_airplane(request):
    """
    Add airplane
    """
    serializer = AirplaneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Successfully added airplane",
            "airplane": serializer.data,
            "actions": {
                "update": f"http://localhost:8000/api/airplanes/update/{serializer.data['id']}",
                "delete": f"http://localhost:8000/api/airplanes/delete/{serializer.data['id']}",
            },
        }
        return Response(response, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="POST", request_body=AirplaneSerializer.many_init())
@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def bulk_add_airplanes(request):
    """
    Add airplane in bulk
    """
    serializer = AirplaneSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        response = {
            "message": "Successfully added airplanes",
            "airplanes": serializer.data,
        }
        return Response(response, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_airplanes(request):
    """
    Get all airplanes
    """
    airplanes = Airplane.objects.all()
    serializer = AirplaneSerializer(airplanes, many=True)
    return Response({"airplanes": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_airplane_by_id(request, id: int):
    """
    Get airplane by id
    """
    try:
        airplane = Airplane.objects.get(pk=id)
        serializer = AirplaneSerializer(airplane)
        response = {
            "airplane": serializer.data,
            "actions": {
                "update": f"http://localhost:8000/api/airplanes/update/{serializer.data['id']}",
                "delete": f"http://localhost:8000/api/airplanes/delete/{serializer.data['id']}",
            },
        }
        return Response(response, status=status.HTTP_200_OK)
    except Airplane.DoesNotExist:
        response = {"message": "Airplane not found"}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method="PUT", request_body=AirplaneSerializer)
@api_view(["PUT"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def update_airplane(request, id: int):
    """
    Update airplane
    """
    try:
        airplane = Airplane.objects.get(pk=id)

        # Check if the ID in the request data is different from the one in the URL
        if request.data["id"] != id:
            serializer = AirplaneSerializer(data=request.data)
            # Delete the older instance
            airplane.delete() if serializer.is_valid() else None
        else:
            serializer = AirplaneSerializer(airplane, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Successfully updated airplane",
                "airplane": serializer.data,
                "actions": {
                    "fetch": f"http://localhost:8000/api/airplanes/{serializer.data['id']}",
                    "delete": f"http://localhost:8000/api/airplanes/delete/{serializer.data['id']}",
                },
            }

            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Airplane.DoesNotExist:
        response = {"message": "Airplane not found"}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_airplane(request, id: int):
    """
    Delete airplane
    """
    try:
        airplane = Airplane.objects.get(pk=id)
        airplane.delete()
        response = {"message": "Successfully deleted airplane"}
        return Response(response, status=status.HTTP_200_OK)
    except Airplane.DoesNotExist:
        response = {"message": "Airplane not found"}
        return Response(response, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def delete_all_airplane(request):
    """
    Delete airplane
    """
    airplanes = Airplane.objects.all()
    if airplanes.count() == 0:
        return Response(
            {"message": "Database already empty"}, status=status.HTTP_200_OK
        )
    airplanes.delete()
    response = {"message": "Successfully deleted all airplanes"}
    return Response(response, status=status.HTTP_200_OK)


# Add rules and users
