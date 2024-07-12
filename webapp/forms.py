from django import forms
from .models import Reserva, Ubicacion, Lugar
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, label='Apellidos', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, required=True, label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nombre de usuario',
            'password1': 'Contraseña',
            'password2': 'Confirmar contraseña',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ['numero', 'estado']

class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['nombre']

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha_reserva', 'fecha_liberacion']
        widgets = {
            'fecha_reserva': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'fecha_liberacion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
