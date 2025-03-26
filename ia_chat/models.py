from django.db import models
from registro.models import Usuario

# Create your models here.

class Conversation(models.Model):
    user = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='conversations')
    initial_prompt = models.TextField()
    generated_prompt = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.user.username} | Initial: {self.initial_prompt} | Response: {self.bot_response}"