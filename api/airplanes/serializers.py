from .models import Airplane
from rest_framework import serializers
import math


class AirplaneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(min_value=1)
    no_of_passengers = serializers.IntegerField(min_value=1)

    class Meta:
        model = Airplane
        fields = "__all__"
        extra_kwargs = {
            "fuel_consumption_per_minute": {"read_only": True},
            "maximum_minutes_to_fly": {"read_only": True},
            "fuel_tank_capacity_in_liters": {"read_only": True},
        }

    def create(self, airplane):
        if Airplane.objects.filter(id=airplane["id"]).exists():
            raise serializers.ValidationError({"id": ("id already exists")})

        airplane = self.calculate_important_fields(airplane)

        return Airplane.objects.create(**airplane)

    def update(self, instance, validated_data):
        if instance.id != validated_data["id"]:
            if Airplane.objects.filter(id=validated_data["id"]).exists():
                raise serializers.ValidationError({"id": ("id already exists")})

        validated_data = self.calculate_important_fields(validated_data)

        instance = super(AirplaneSerializer, self).update(instance, validated_data)
        instance.save()
        return instance

    def calculate_important_fields(self, airplane: dict) -> dict:
        id = airplane["id"]
        passengers = airplane["no_of_passengers"]
        # fmt: off
        # get fuel tank capacity
        airplane["fuel_tank_capacity_in_liters"] = self.get_fuel_tank_capacitiy_in_liters(id)

        # get fuel consumption per minute
        airplane["fuel_consumption_per_minute"] = self.get_fuel_consumption_per_minute(id, passengers)

        # get maximum minutes to fly
        airplane["maximum_minutes_to_fly"] = self.get_maximum_minutes_to_fly(
            airplane["fuel_tank_capacity_in_liters"],
            airplane["fuel_consumption_per_minute"],
        )

        return airplane

    def get_fuel_tank_capacitiy_in_liters(self, id: int) -> float:
        return id * 200

    def get_fuel_consumption_per_minute(self, id: int, passengers: int) -> float:
        normal_airplane_consumption: float = math.log(id) * 0.80
        additional_consumption_per_passenger: float = 0.002 * passengers
        return normal_airplane_consumption + additional_consumption_per_passenger

    # fmt: off
    def get_maximum_minutes_to_fly(self, tank_capacity: float, fuel_consumption: float) -> float:
        return tank_capacity / fuel_consumption
