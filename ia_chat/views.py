from django.shortcuts import render
import requests
from .models import Conversation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

def generate_prompt(initial_prompt):
    """
    Genera un prompt más elaborado en base al prompt inicial.
    """
    profesion = "programador python"
    fin_uso = "Escribir codigo limpio y optimo"
    generated_prompt = f"""
    Crea un prompt optimo en base a los siguientes datos:
    - Profesión: {profesion}
    - Finalidad de uso: {fin_uso}
    - prompt inicial: {initial_prompt}
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
    def post(self, request, *args, **kwargs):
        # Paso 1: Obtener el prompt inicial del usuario
        initial_prompt = request.data.get('initial_prompt')
        if not initial_prompt:
            return Response(
                {'error': 'El campo "initial_prompt" es requerido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Paso 2: Generar un prompt más elaborado
        generated_prompt = generate_prompt(initial_prompt)

        # Paso 3: Generar un prompt final (opcional, según tu lógica)
        final_prompt = ask_ollama(generated_prompt)

        # Paso 4: Enviar el prompt final a Ollama y obtener la respuesta
        bot_response = ask_ollama(final_prompt)

        # Paso 5: Guardar la conversación en la base de datos
        Conversation.objects.create(
            initial_prompt=initial_prompt,
            generated_prompt=final_prompt,
            bot_response=bot_response
        )

        # Paso 6: Retornar la respuesta al usuario
        return Response({
            'initial_prompt': initial_prompt,
            'generated_prompt': final_prompt,
            'bot_response': bot_response
        }, status=status.HTTP_200_OK)