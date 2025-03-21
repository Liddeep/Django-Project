from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from registro.models import Usuario
from .serializers import UsuarioGestionSerializer
from .permissions import IsprofileOwner
import requests

# Create your views here.

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def ObtenerPerfil(request):
    try:
        usuario = Usuario.objects.get(id=request.user.id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = UsuarioGestionSerializer(usuario)
    return Response(serializer.data)
    
@api_view(['PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated, IsprofileOwner])
def ActualizarPerfil(request):
    try:
        usuario = Usuario.objects.get(id=request.user.id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = UsuarioGestionSerializer(usuario, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Perfil actualizado exitosamente.'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requiere autenticación
def ia_endpoint(request):
    """
    Endpoint para interactuar con la IA, pasando el contexto del paciente.
    """
    try:
        paciente_id = request.data.get('paciente_id')  # Obtiene el ID del paciente desde la solicitud
        prompt = request.data.get('prompt')  # Obtiene el prompt desde la solicitud

        if not paciente_id or not prompt:
            return Response({"error": "Se requiere paciente_id y prompt."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            paciente = Usuario.objects.get(pk=paciente_id)
        except Usuario.DoesNotExist:
            return Response({"error": "Paciente no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UsuarioGestionSerializer(paciente)
        paciente_data = serializer.data  # Datos serializados del paciente

        # Prepara los datos para enviar a la IA
        ia_payload = {
            "prompt": prompt,
            "context": paciente_data  # Incluye los datos del paciente como contexto
        }

        # **Importante:** Reemplaza con la URL de tu servidor de IA
        ia_url = "http://localhost:8000/ia_api"  # Ejemplo
        try:
            ia_response = requests.post(ia_url, json=ia_payload)
            ia_response.raise_for_status()  # Lanza una excepción para códigos de error HTTP
            ia_response_data = ia_response.json()  # Parsea la respuesta JSON
            return Response(ia_response_data, status=status.HTTP_200_OK)  # Devuelve la respuesta de la IA
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Error al contactar la IA: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValueError:
            return Response({"error": "Respuesta de la IA no es un JSON válido."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
