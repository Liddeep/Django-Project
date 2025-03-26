from django.shortcuts import render
import requests
from .models import Conversation
from rest_framework.decorators import APIView, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

def generate_prompt(initial_prompt, user):
    """
    Genera un prompt más elaborado en base al prompt inicial y la información del usuario.
    """
    # Accede a la información del usuario
    username = user.username
    first_name = user.first_name
    last_name = user.last_name
    email = user.email






    # Formatea el prompt
    generated_prompt = f"""
    Crea un prompt optimo en base a los siguientes datos:
    - Nombre de usuario: {username}
    - Nombre: {first_name}
    - Apellido: {last_name}
    - Email: {email}
    - Profesión: {profesion}
    - Finalidad de uso: {fin_uso}
    - Prompt inicial: {initial_prompt}
    """



    return generated_prompt.strip()

def ask_ollama(prompt):
    """
    Envía un prompt a Ollama y obtiene la respuesta del modelo.
    """
    response = requests.post(
        'http://localhost:11434/api/generate',  # Endpoint de Ollama
        json={
            "model": "gemma",  # Modelo a usar (puedes cambiarlo)
            "prompt": prompt,
            "stream": False  # Para obtener una respuesta completa
        }
    )

    if response.status_code == 200:
        return response.json()['response']
    else:
        return "Error: No se pudo obtener una respuesta del modelo."

class ProcessPromptView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Paso 1: Obtener el prompt inicial del usuario
        initial_prompt = request.data.get('initial_prompt')
        if not initial_prompt:
            return Response(
                {'error': 'El campo "initial_prompt" es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 2: Generar un prompt más elaborado utilizando la información del usuario
        generated_prompt = generate_prompt(initial_prompt, request.user) # Pasar el usuario

        # Paso 3: Enviar el prompt final a Ollama y obtener la respuesta
        bot_response = ask_ollama(generated_prompt)

        # Paso 4: Guardar la conversación en la base de datos
        conversation = Conversation.objects.create(
            initial_prompt=initial_prompt,
            generated_prompt=generated_prompt,
            bot_response=bot_response
        )

        # Paso 5: Retornar la respuesta al usuario
        return Response({
            'initial_prompt': initial_prompt,
            'generated_prompt': generated_prompt,
            'bot_response': bot_response
        }, status=status.HTTP_200_OK)
