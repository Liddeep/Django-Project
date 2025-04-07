from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    edad = models.IntegerField(blank=True, null=True)
    sexo = models.CharField(blank=True, null=True, max_length=1, choices=[
        ('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')
    ])
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_de_sangre = models.CharField(blank=True, null=True, max_length=3, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])
    direccion = models.CharField(blank=True, null=True, max_length=255)
    telefono = models.CharField(blank=True, null=True, max_length=11)
    alergias = models.TextField(blank=True, null=True)
    antecedentes_medicos = models.TextField(blank=True, null=True)
    medicacion = models.TextField(blank=True, null=True)
    historial_vacunas = models.TextField(blank=True, null=True)
    enfermedades = models.TextField(blank=True, null=True)
    sintomas = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.tipo_de_sangre} - {self.alergias} - {self.antecedentes_medicos}'
