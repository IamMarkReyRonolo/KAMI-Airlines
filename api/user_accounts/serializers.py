from rest_framework import serializers
from .models import KAMIUser
from django.db import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = KAMIUser
        fields = ["first_name", "last_name", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if KAMIUser.objects.filter(email=attrs["username"]).exists():
            serializers.ValidationError({"error": ("Username already exists")})

        return super().validate(attrs)


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = KAMIUser
        fields = ["username", "password"]


class PayloadSerializer(serializers.ModelSerializer):
    is_authenticated: serializers.BooleanField()
    name: serializers.CharField()

    class Meta:
        model = KAMIUser
        fields = ["id", "name", "username", "is_authenticated"]
