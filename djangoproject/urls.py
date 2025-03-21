"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from registro.views import RegistrarUsuario
from gestion.views import ObtenerPerfil, ActualizarPerfil, ia_endpoint
from login.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegistrarUsuario, name='Registro de Usuario'),
    path('api/user/', ObtenerPerfil, name='perfil_usuario'),
    path('api/user/edit/', ActualizarPerfil, name='modificar_perfil'),
    path('ia/', ia_endpoint, name='chat_ia'),
    path('api/login/', login_view, name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
