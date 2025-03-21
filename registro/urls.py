'''
from django.urls import path
from .views import registrar_usuario

urlpatterns = [
    path('registro/', registrar_usuario, name='registro'),
]
'''