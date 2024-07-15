from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import Ubicacion, Lugar, Reserva
    
class UbicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ubicacion
        fields = '__all__'

class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ['cliente']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("El usuario esta deshabilitado.")
                data['user'] = user
            else:
                raise serializers.ValidationError("No se puede iniciar sesión con esas credenciales.")
        else:
            raise serializers.ValidationError("Debes incluir usuario y contraseña")

        return data
