from django.shortcuts import render
import requests
from .models import Conversation
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from control_panel.models import ControlPanel
import os


def generate_prompt(initial_prompt, user):
    """
    Genera un prompt más elaborado en base al prompt inicial y a la información del usuario.
    """

    try:
        # Obtener las instrucciones del ControlPanel
        control_panel = ControlPanel.objects.filter(user=user).first()
        system_prompt = (
            control_panel.system_prompt
            if control_panel and control_panel.system_prompt
            else (
                "Eres un asistente médico especializado en análisis de datos médicos. "
                "Tu tarea es analizar la siguiente consulta (o pregunta) y proporcionar una respuesta profesional y útil."
            )
        )
    except Exception as e:
        system_prompt = (
            "Eres un asistente médico especializado en análisis de datos médicos. "
            "Tu tarea es analizar la siguiente consulta (o pregunta) y proporcionar una respuesta profesional y útil."
        )

    # Formateo del prompt
    generated_prompt = f"""
    {system_prompt}
     
    **Información del paciente del Paciente:**
    Nombre               = {user.first_name} {user.last_name}
    Email                = {user.email}
    Número               = {user.telefono}
    tipo_de_sangre       = {user.tipo_de_sangre}
    alergias             = {user.alergias}
    antecedentes_medicos = {user.antecedentes_medicos}
    medicacion           = {user.medicacion}
    historial_de_vacunas = {user.historial_vacunas}
    sintomas             = {user.sintomas}

    **contulta o pregunta del doctor a cargo:**
    "{initial_prompt}"
    
    """
    return generated_prompt.strip(), "system_prompt"


def ask_ollama(prompt, user):
    """
    Envía un prompt a Ollama y obtiene la respuesta del modelo.
    """
    
    try:
        # Obtener la configuración del ControlPanel
        control_panel = ControlPanel.objects.filter(user=user).first()
        temperature = control_panel.temperature if control_panel else 0.7  # Valor por defecto
        max_tokens = control_panel.max_tokens if control_panel else 2048  # Valor por defecto
    except Exception as e:
        return f"Error al obtener configuración: {str(e)}"

    payload = {
        "model": "gemma3:1b",  # Modelo a usar (puedes cambiarlo)
        "prompt": prompt,
        "temperature": temperature,  # Parámetro opcional para controlar la creatividad
        "max_tokens": max_tokens,  # Máximo de tokens en la respuesta
        "stream": False,  # Para obtener una respuesta completa
    }
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",  # Endpoint de Ollama
            json=payload,
        )

        if response.status_code == 200:
            return response.json()["response"]
        else:
            return "Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error en la conexión: {str(e)}"

def ask_deepseek(prompt, user):
    """
    Envía un prompt a la API de DeepSeek y obtiene la respuesta del modelo.
    """
    # Configuración de la API de DeepSeek
    headers = {"Authorization": os.getenv("ia_key"), "Content-Type": "application/json"}

    # Obtener la configuración del ControlPanel
    try:
        control_panel = ControlPanel.objects.filter(user=user).first()  # Corrección del método
        temperature = control_panel.temperature if control_panel else 0.7  # Valor por defecto
        max_tokens = control_panel.max_tokens if control_panel else 2048  # Valor por defecto
    except Exception as e:
        return f"Error al obtener configuración: {str(e)}"

    payload = {
        "model": "deepseek-chat",  # Modelo de DeepSeek
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,  # Parámetro opcional para controlar la creatividad
        "max_tokens": max_tokens,  # Máximo de tokens en la respuesta
    }

    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",  # Endpoint de DeepSeek
            headers=headers,
            json=payload,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error en la conexión: {str(e)}"


class ProcessPromptView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Paso 1: Obtener el prompt inicial del usuario
        initial_prompt = request.data.get("initial_prompt")
        if not initial_prompt:
            return Response(
                {"error": 'El campo "initial_prompt" es requerido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Paso 2: Obtener el límite de mensajes del contexto desde el ControlPanel
        try:
            control_panel = ControlPanel.objects.filter(user=request.user).first()
            context_length = control_panel.context_length if control_panel else 20  # Valor por defecto
        except Exception as e:
            return Response(
                {"error": f"Error al obtener el contexto: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Paso 3: Recuperar los mensajes más recientes de la conversación
        recent_messages = Conversation.objects.filter(user=request.user).order_by(
            "-timestamp"
        )[:context_length]

        # Paso 4: Formatear los mensajes del contexto
        context_messages = "\n".join(
            [
                f"Usuario: {msg.initial_prompt}\nAsistente: {msg.bot_response}"
                for msg in recent_messages
            ]
        )

        # Paso 5: Generar un prompt más elaborado
        generated_prompt, _ = generate_prompt(initial_prompt, request.user)  # Corrección: se desestructura el retorno
        final_prompt = f"{context_messages}\n\n{generated_prompt}"

        # Paso 6: Generar un prompt final (opcional, según tu lógica)
        try:
            final_prompt = ask_deepseek(
                f"Por favor mejora el siguiente prompt (sin hacer ninguna referencia a que es un prompt mejorado): {generated_prompt}",
                request.user,  # Corrección: se pasa el usuario como argumento
            )
        except Exception as e:
            return Response(
                {"error": f"Error al mejorar el prompt: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Paso 7: Enviar el prompt final a Ollama y obtener la respuesta
        try:
            bot_response = ask_deepseek(final_prompt, request.user)  # Corrección: se pasa el usuario como argumento
        except Exception as e:
            return Response(
                {"error": f"Error al obtener la respuesta del modelo: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Paso 8: Guardar la conversación en la base de datos
        conversation = Conversation.objects.create(
            user=request.user,
            initial_prompt=initial_prompt,
            generated_prompt=generated_prompt,
            bot_response=bot_response,
        )

        # Paso 9: Retornar la respuesta al usuario
        return Response(
            {
                "initial_prompt": initial_prompt,
                "bot_response": bot_response,
                "conversation_id": conversation.id,
            },
            status=status.HTTP_200_OK,
        )
