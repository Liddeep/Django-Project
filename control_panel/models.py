from django.db import models
from registro.models import Usuario

# Create your models here.
class ControlPanel(models.Model):
    """
    Modelo para almacenar información sobre el panel de control del chat de IA.
    Permite configurar diferentes instancias de chat con parámetros personalizados.
    """
    name = models.CharField(max_length=255, verbose_name="Nombre del Panel")
    description = models.TextField(verbose_name="Descripción del Panel")
    
    # Usuario propietario (opcional)
    user = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name="Usuario Propietario",
        related_name="control_panels"
    )
    
    # Parámetros del modelo de IA
    temperature = models.FloatField(
        default=0.7, 
        verbose_name="Temperatura"
    )
    max_tokens = models.IntegerField(
        default=2048, 
        verbose_name="Máximo de Tokens"
    )
    
    # Configuración del contexto
    system_prompt = models.TextField(
        blank=True, 
        verbose_name="Prompt del Sistema", 
        help_text="Instrucciones iniciales para el asistente"
    )
    context_length = models.IntegerField(
        default=20, 
        verbose_name="Longitud del Contexto", 
        help_text="Número de mensajes a mantener en el contexto"
    )
    
    # Configuración de funcionalidades
    save_chat_history = models.BooleanField(
        default=True, 
        verbose_name="Guardar Historial de Chat"
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name="Activo"
    )
    
    # Campos de auditoría
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Actualización"
    )
    class Meta:
        verbose_name = "Panel de Control"
        verbose_name_plural = "Paneles de Control"

class ChatSessions(models.Model):
    """
    Modelo para almacenar sesiones de chat individuales.
    """
    panel = models.ForeignKey(
        ControlPanel, 
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    user = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE,
        related_name="chat_sessions"
    )
    title = models.CharField(
        max_length=255, 
        default="Nueva conversación",
        verbose_name="Título"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    last_activity = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actividad"
    )
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        verbose_name = "Sesión de Chat"
        verbose_name_plural = "Sesiones de Chat"
        ordering = ['-last_activity']