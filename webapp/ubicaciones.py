from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ubicacion, Lugar
from .forms import UbicacionForm, LugarForm
from django.contrib import messages

# Verificar si el usuario es administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff

# Vista para listar ubicaciones
@login_required
def lista_ubicaciones(request):
    ubicaciones = Ubicacion.objects.all()
    return render(request, 'ubicaciones/lista_ubicaciones.html', {'ubicaciones': ubicaciones})

# Vista para crear una nueva ubicación (solo para administradores)
@login_required
@user_passes_test(is_admin)
def crear_ubicacion(request):
    if request.method == 'POST':
        form = UbicacionForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            if Ubicacion.objects.filter(nombre=nombre).exists():
                messages.error(request, "Ya existe una ubicación con este nombre.")
            else:
                form.save()
                messages.success(request, "Ubicación creada exitosamente.")
                return redirect('lista_ubicaciones')
    else:
        form = UbicacionForm()
    return render(request, 'ubicaciones/crear_ubicacion.html', {'form': form})
# Vista para eliminar una ubicación (solo para administradores)
@login_required
@user_passes_test(is_admin)
def eliminar_ubicacion(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
    if request.method == 'POST':
        ubicacion.delete()
        messages.success(request, "Ubicación eliminada exitosamente.")
        return redirect('lista_ubicaciones')
    return render(request, 'ubicaciones/eliminar_ubicacion.html', {'ubicacion': ubicacion})
