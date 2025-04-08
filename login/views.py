import requests
from django.conf import settings
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from django.middleware.csrf import get_token
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_jwt_tokens(username, password):
    """
    Realiza una solicitud POST al endpoint JWT definido en settings para obtener
    el par de tokens (access y refresh).
    """
    try:
        response = requests.post(
            settings.JWT_AUTH_URL,
            data={"username": username, "password": password},
            timeout=5,
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("access"), data.get("refresh")
    except requests.exceptions.RequestException:
        return None, None
    return None, None


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Obtener tokens del endpoint externo
    access_token, refresh_token = get_jwt_tokens(
        serializer.validated_data["username"], request.data.get("password")
    )

    if not access_token:
        return Response(
            {"error": "Falló la obtención de tokens JWT"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    return Response(
        {
            "access": access_token,
            "refresh": refresh_token,
            "redirect_url": "/api/user/",
        },
        status=status.HTTP_200_OK,
    )
