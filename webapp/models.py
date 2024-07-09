from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)

class Lugar(models.Model):
    numero = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="libre")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)


class Reserva(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(null=True, blank=True)
    fecha_liberacion = models.DateTimeField(null=True, blank=True)