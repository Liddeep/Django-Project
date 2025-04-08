from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()


class UsuarioSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmacion = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ("id", "username", "email", "password", "password_confirmacion")

    def validate(self, data):
        if data["password"] != data["password_confirmacion"]:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        return data

    def create(self, validated_data):
        validated_data.pop("password_confirmacion")
        password = validated_data.pop("password")
        usuario = Usuario(**validated_data)
        usuario.set_password(password)
        usuario.save()
        return usuario
