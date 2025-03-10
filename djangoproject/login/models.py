from django.db import models
from django.contrib.auth import get_user_model

#  Create your models here.

User = get_user_model()

class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField(blank=True, null=True)
    refresh_token = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Tokens de {self.user.username}"


