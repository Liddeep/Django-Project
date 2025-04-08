from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UsuarioSerializer

# Create your views here.


@api_view(["POST"])
def RegistrarUsuario(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {"mensaje": "Usuario registrado exitosamente."},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
