from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if not user:
            raise serializers.ValidationError("Credenciales inválidas.")

        data["user"] = user
        return data
