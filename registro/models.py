from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    tipo_de_sangre = models.CharField(blank=True, null=True, max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    telefono = models.CharField(blank=True, null=True, max_length=11)
    alergias = models.TextField(blank=True, null=True)
    antecedentes_medicos = models.TextField(blank=True, null=True)
    medicacion = models.TextField(blank=True, null=True)
    historial_vacunas = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo_de_sangre} - {self.alergias} - {self.antecedentes_medicos}'
