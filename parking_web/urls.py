
from django.contrib import admin
from django.urls import path
from webapp import inicio, lugares


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio.inicio, name='inicio'),
    path('iniciar_sesion/', inicio.iniciar_sesion, name='iniciar_sesion'),
    path('registrar_usuario/', inicio.registrar_usuario, name='registrar_usuario'),
    path('bienvenida/', inicio.bienvenida, name='bienvenida'),
    path('panel/', inicio.panel, name='panel'),
    path('cerrar_sesion/', inicio.cerrar_sesion, name='cerrar_sesion'),
]
