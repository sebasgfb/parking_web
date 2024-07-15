from django.contrib import admin
from .models import Lugar, Reserva, Ubicacion

class UbicacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',) 

class LugarAdmin(admin.ModelAdmin):
    list_display = ('numero', 'get_ubicacion_nombre')  # Muestra número y nombre de la ubicación en el admin

    def get_ubicacion_nombre(self, obj):
        return obj.ubicacion.nombre

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('fecha_reserva',)

admin.site.register(Ubicacion, UbicacionAdmin)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(Reserva, ReservaAdmin)