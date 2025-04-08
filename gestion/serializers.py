from rest_framework import serializers
from registro.models import Usuario


class UsuarioGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "edad",
            "sexo",
            "fecha_nacimiento",
            "tipo_de_sangre",
            "direccion",
            "telefono",
            "alergias",
            "antecedentes_medicos",
            "medicacion",
            "historial_vacunas",
            "enfermedades",
            "sintomas",
        ]
        read_only_fields = ["id", "username"]
