from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  # Agrega esta línea
from .models import PerfilUsuario

class CustomUserCreationForm(UserCreationForm):
    campopersonalizado = forms.CharField(max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('campopersonalizado',)
