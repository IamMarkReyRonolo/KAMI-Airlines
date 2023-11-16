from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Airplane
from .serializers import AirplaneSerializer
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method="POST", request_body=AirplaneSerializer)
@api_view(["POST"])
def add_airplane(request):
    """
    Add airplane
    """
    serializer = AirplaneSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        message = {
            "message": "Successfully added airplane",
            "airplane": serializer.data,
        }
        return Response(message, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method="POST", request_body=AirplaneSerializer.many_init())
@api_view(["POST"])
def bulk_add_airplanes(request):
    """
    Add airplane in bulk
    """
    serializer = AirplaneSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        message = {
            "message": "Successfully added airplanes",
            "airplanes": serializer.data,
        }
        return Response(message, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all_airplanes(request):
    """
    Get all airplanes
    """
    airplanes = Airplane.objects.all()
    serializer = AirplaneSerializer(airplanes, many=True)
    return Response({"airplanes": serializer.data}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_airplane_by_id(request, id: int):
    """
    Get airplane by id
    """
    try:
        airplane = Airplane.objects.get(pk=id)
        serializer = AirplaneSerializer(airplane)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Airplane.DoesNotExist:
        message = {"message": "Airplane not found"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method="PUT", request_body=AirplaneSerializer)
@api_view(["PUT"])
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
            message = {
                "message": "Successfully updated airplane",
                "airplane": serializer.data,
            }

            return Response(message)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Airplane.DoesNotExist:
        message = {"message": "Airplane not found"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
def delete_airplane(request, id: int):
    """
    Delete airplane
    """
    try:
        airplane = Airplane.objects.get(pk=id)
        airplane.delete()
        message = {"message": "Successfully deleted airplane"}
        return Response(message, status=status.HTTP_200_OK)
    except Airplane.DoesNotExist:
        message = {"message": "Airplane not found"}
        return Response(message, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
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
    message = {"message": "Successfully deleted all airplanes"}
    return Response(message, status=status.HTTP_200_OK)


# Add rules and users
