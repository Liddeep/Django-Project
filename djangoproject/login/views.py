import requests
from django.conf import settings
from django.contrib.auth import login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import UserToken
from .serializers import LoginSerializer
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny

def get_jwt_tokens(username, password):
    """
    Realiza una solicitud POST al endpoint JWT definido en settings para obtener
    el par de tokens (access y refresh).
    """
    jwt_url = settings.JWT_AUTH_URL
    payload = {
        'username': username,
        'password': password
    }
    response = requests.post(jwt_url, data=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get('access'), data.get('refresh')
    return None, None

@api_view(['POST'])
@permission_classes([AllowAny])  # Permite el acceso sin autenticación
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    user = serializer.validated_data['user']
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        if user is None:
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        elif user is not None:
            login(request, user) # Inicia la sesión en Django (si se requiere mantenerla) para establecer la cookie CSRF
            
            # Obtiene o crea los tokens JWT
            access_token, refresh_token = get_jwt_tokens(username, password)
            if not access_token or not refresh_token:
                return Response(
                    {"error": "No se pudieron obtener los tokens de autenticación."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            UserToken.objects.update_or_create(
                user=user,
                defaults={
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            )
            
            # Obtiene el token CSRF
            csrf_token = get_token(request)

            return Response(
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "csrf_token": csrf_token,
                    "redirect_url": "/api/user/"
                },
                status=status.HTTP_200_OK
            )
        
        else:
            return Response(
                {"error": "Credenciales inválidas."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
    return Response(
    {"error": "Método no permitido."},
    status=status.HTTP_405_METHOD_NOT_ALLOWED
    )