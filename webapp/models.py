from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campopersonalizado = models.CharField(max_length=100)

class Lugar(models.Model):
    
    numero = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="libre")
    ubicacion = models.CharField(max_length=100)


class Reserva(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    fecha_liberacion = models.DateTimeField(null=True, blank=True)