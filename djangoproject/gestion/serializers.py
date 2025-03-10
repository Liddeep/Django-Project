from rest_framework import serializers
from registro.models import Usuario

class UsuarioGestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name','telefono', 'tipo_de_sangre', 'alergias','antecedentes_medicos', 'medicacion', 'historial_vacunas']
        read_only_fields = ['id', 'username']
