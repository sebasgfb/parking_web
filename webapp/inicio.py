from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import PerfilUsuario, Reserva, Lugar
from .forms import CustomUserCreationForm

def inicio(request):
    return render(request, 'inicio.html')

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('panel')  
    else:
        form = AuthenticationForm()
    return render(request, 'iniciar_sesion.html', {'form': form})

def registrar_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            perfil_usuario = PerfilUsuario(usuario=user, campopersonalizado=form.cleaned_data.get('campopersonalizado'))
            perfil_usuario.save()
            login(request, user)
            return redirect('panel')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registrar_usuario.html', {'form': form})



@login_required

def panel(request):
    usuario = request.user
    reservas = Reserva.objects.filter(cliente=usuario)
    lugares_disponibles = Lugar.objects.filter(estado='libre')  # Obtener lugares disponibles
    return render(request, 'panel.html', {'reservas': reservas, 'lugares_disponibles': lugares_disponibles})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')
