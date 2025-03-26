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
    Genera un prompt más elaborado en base al prompt inicial y a la información del usuario.
    """
    # Accede a la información del usuario
    first_name = user.first_name
    last_name = user.last_name
    email = user.email
    tipo_de_sangre = user.tipo_de_sangre
    alergias = user.alergias
    antecedentes_medicos = user.antecedentes_medicos
    medicacion = user.medicacion
    historial_de_vacunas = user.historialvacunas
    sintomas = user.sintomas
    
    # Formateo del prompt
    generated_prompt = f"""
    Crea un prompt optimo en base a los siguientes datos:
    - Nombre del paciente: {first_name}
    - Apellido del paciente: {last_name}
    - Correo electronico del paciente: {email}
    - Tipo de sangre del paciente: {tipo_de_sangre}
    - Alergias del paciente: {alergias}
    - Antecendentes medicos del paciente: {antecedentes_medicos}
    - Medicación del paciente: {medicacion}
    - Historial de vacunas del paciente: {historial_de_vacunas}
    - Sintomas del paciente: {sintomas}
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

        # Paso 2: Generar un prompt más elaborado
        generated_prompt = generate_prompt(initial_prompt, request.user)

        # Paso 3: Generar un prompt final (opcional, según tu lógica)
        final_prompt = ask_ollama(generated_prompt)

        # Paso 4: Enviar el prompt final a Ollama y obtener la respuesta
        bot_response = ask_ollama(final_prompt)

        # Paso 5: Guardar la conversación en la base de datos
        Conversation.objects.create(
            user=request.user,
            initial_prompt=initial_prompt,
            generated_prompt=final_prompt,
            bot_response=bot_response
        )

        # Paso 6: Retornar la respuesta al usuario
        return Response({
            'initial_prompt': initial_prompt,
            'generated_prompt': final_prompt,
            'bot_response': bot_response,
            'conversation_id': Conversation.id,
        }, status=status.HTTP_200_OK)