from django.urls import path
from . import views

urlpatterns = [
    path('perfil/', views.PerfilUsuario, name='perfil_usuario'),
    path('ia/', views.ia_endpoint, name='ia_endpoint'),
]
