from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Ubicacion(models.Model):
    nombre = models.CharField(max_length=100)

class Lugar(models.Model):
    numero = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, default="libre")
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE)

    def actualizar_estado(self):
        ahora = timezone.now()
        reservas = self.reserva_set.filter(fecha_reserva__lte=ahora, fecha_liberacion__gte=ahora)
        if reservas.exists():
            self.estado = "Ocupado"
        else:
            self.estado = "Libre"
        self.save()

        # Eliminar reservas pasadas
        reservas_pasadas = self.reserva_set.filter(fecha_liberacion__lt=ahora)
        reservas_pasadas.delete()


class Reserva(models.Model):
    lugar = models.ForeignKey(Lugar, on_delete=models.CASCADE)
    cliente = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(null=True, blank=True)
    fecha_liberacion = models.DateTimeField(null=True, blank=True)