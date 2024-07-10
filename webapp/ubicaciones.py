from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ubicacion, Lugar
from .forms import UbicacionForm, LugarForm

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
            form.save()
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
        return redirect('lista_ubicaciones')
    return render(request, 'ubicaciones/eliminar_ubicacion.html', {'ubicacion': ubicacion})

# Vista para listar lugares de una ubicación
@login_required
def lista_lugares(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
    lugares = Lugar.objects.filter(ubicacion=ubicacion)
    return render(request, 'lugares/lista_lugares.html', {'ubicacion': ubicacion, 'lugares': lugares})

# Vista para crear un nuevo lugar en una ubicación (solo para administradores)
@login_required
@user_passes_test(is_admin)
def crear_lugar(request, ubicacion_id):
    ubicacion = get_object_or_404(Ubicacion, id=ubicacion_id)
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
            lugar = form.save(commit=False)
            lugar.ubicacion = ubicacion
            lugar.save()
            return redirect('lista_lugares', ubicacion_id=ubicacion.id)
    else:
        form = LugarForm()
    return render(request, 'lugares/crear_lugar.html', {'ubicacion': ubicacion, 'form': form})


# Vista para eliminar un lugar (solo para administradores)
@login_required
@user_passes_test(is_admin)
def eliminar_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    ubicacion_id = lugar.ubicacion.id  # Guardamos el ID de la ubicación para redireccionar después
    if request.method == 'POST':
        lugar.delete()
        return redirect('lista_lugares', ubicacion_id=ubicacion_id)
    return render(request, 'lugares/eliminar_lugar.html', {'lugar': lugar})
