from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .models import Ubicacion, Lugar, Reserva
from .serializers import UbicacionSerializer, LugarSerializer, ReservaSerializer, UserSerializer, LoginSerializer

@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response(serializer.errors, status=400)
    
@api_view(['POST'])
def logout_view(request):
    try:
        # Obtener el token de autenticación del encabezado Authorization
        auth_token = request.headers.get('Authorization', '').split(' ')[1]

        # Buscar el token en la base de datos
        token = Token.objects.get(key=auth_token)

        # Eliminar el token
        token.delete()

        return Response({'detail': 'Logout exitoso'}, status=status.HTTP_200_OK)

    except Token.DoesNotExist:
        return Response({'detail': 'Token inválido'}, status=status.HTTP_400_BAD_REQUEST)

    except IndexError:
        return Response({'detail': 'Token no proporcionado en el encabezado'}, status=status.HTTP_400_BAD_REQUEST)

    
class UbicacionViewSet(viewsets.ModelViewSet):
    queryset = Ubicacion.objects.all()
    serializer_class = UbicacionSerializer

class LugarViewSet(viewsets.ModelViewSet):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer

    @action(detail=True, methods=['get'], url_path='lugares')
    def ubicaciones(self, request, pk=None):
        lugares = Lugar.objects.filter(ubicacion=pk)
        serializer = self.get_serializer(lugares, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='reservas')
    def reservas(self, request, pk=None):
        reservas = Reserva.objects.filter(lugar=pk)
        serializer = ReservaSerializer(reservas, many=True)
        return Response(serializer.data)

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # Filtrar solo usuarios no administradores
    serializer_class = UserSerializer

