from django.contrib import admin
from django.urls import path, include
from webapp import inicio, ubicaciones, lugares, reservas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio.inicio, name='inicio'),
    path('iniciar_sesion/', inicio.iniciar_sesion, name='iniciar_sesion'),
    path('registrar_usuario/', inicio.registrar_usuario, name='registrar_usuario'),
    path('bienvenida/', inicio.bienvenida, name='bienvenida'),
    path('cerrar_sesion/', inicio.cerrar_sesion, name='cerrar_sesion'),
    path('ubicaciones/', ubicaciones.lista_ubicaciones, name='lista_ubicaciones'),
    path('ubicaciones/crear/', ubicaciones.crear_ubicacion, name='crear_ubicacion'),
    path('ubicaciones/eliminar/<int:ubicacion_id>/', ubicaciones.eliminar_ubicacion, name='eliminar_ubicacion'),
    path('ubicaciones/modificar/<int:ubicacion_id>/', ubicaciones.modificar_ubicacion, name='modificar_ubicacion'),
    path('ubicaciones/<int:ubicacion_id>/lugares/', lugares.lista_lugares, name='lista_lugares'),
    path('ubicaciones/<int:ubicacion_id>/lugares/crear/', lugares.crear_lugar, name='crear_lugar'),
    path('ubicaciones/lugares/eliminar/<int:lugar_id>/', lugares.eliminar_lugar, name='eliminar_lugar'),
    path('ubicaciones/lugares/modificar/<int:lugar_id>/', lugares.modificar_lugar, name='modificar_lugar'),
    path('lugar/<int:lugar_id>/reservas', reservas.detalle_lugar, name='detalle_lugar'),
    path('reservas/eliminar/<int:reserva_id>/', reservas.eliminar_reserva, name='eliminar_reserva'),
    path('reservas/modificar/<int:reserva_id>/', reservas.modificar_reserva, name='modificar_reserva'),
    path('api/', include('parking_web.urls_api')), 
]
