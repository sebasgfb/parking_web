from django.urls import path, include
from rest_framework.routers import DefaultRouter
from webapp.views_api import UbicacionViewSet, LugarViewSet, ReservaViewSet, UserViewSet, login_view, logout_view

router = DefaultRouter()
router.register(r'ubicaciones', UbicacionViewSet)
router.register(r'lugares', LugarViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'usuarios', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]