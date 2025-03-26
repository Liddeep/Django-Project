from django.db import models

# Create your models here.

class Conversation(models.Model):
    initial_prompt = models.TextField()
    generated_prompt = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    # user = models.ManyToManyField("auth.User")

    def __str__(self):
        return f"Initial: {self.initial_prompt} | Response: {self.bot_response}"