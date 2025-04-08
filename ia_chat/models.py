from django.db import models
from registro.models import Usuario
from control_panel.models import ChatSessions

# Create your models here.


class Conversation(models.Model):
    user = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="conversations"
    )
    initial_prompt = models.TextField()
    generated_prompt = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username} | Initial: {self.initial_prompt} | Response: {self.bot_response}"

    def get_context_messages(self):
        """
        Recupera los mensajes más recientes de la sesión de chat,
        respetando el límite definido en el ControlPanel.
        """
        try:
            control_panel = (
                self.user.control_panels.first()
            )  # Obtén el panel de control del usuario
            context_length = (
                control_panel.context_length if control_panel else 10
            )  # Valor por defecto
            session = ChatSessions.objects.filter(
                user=self.user
            ).first()  # Obtén la sesión de chat
            if session:
                return session.messages.all().order_by("-created_at")[:context_length]
            return []
        except Exception as e:
            # Manejo de errores
            return ["error"]
