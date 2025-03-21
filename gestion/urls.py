from django.urls import path
from .views import PerfilUsuario

urlpatterns = [
    path('perfil/', PerfilUsuario, name='perfil_usuario'),
]
