from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Ubicacion, Lugar
from .forms import LugarForm
from django.contrib import messages


# Verificar si el usuario es administrador
def is_admin(user):
    return user.is_authenticated and user.is_staff

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
            numero = form.cleaned_data['numero']
            
            # Verificar si ya existe un lugar con el mismo número en esta ubicación
            if Lugar.objects.filter(ubicacion=ubicacion, numero=numero).exists():
                messages.error(request, 'Ya existe un lugar con este número en esta ubicación.')
            else:
                lugar = form.save(commit=False)
                lugar.ubicacion = ubicacion
                lugar.save()
                messages.success(request, 'Lugar creado exitosamente.')
                return redirect('lista_lugares', ubicacion_id=ubicacion.id)
        else:
            messages.error(request, 'Corrija los errores indicados.')
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
        messages.success(request, 'Lugar eliminado exitosamente.')
        return redirect('lista_lugares', ubicacion_id=ubicacion_id)
    return render(request, 'lugares/eliminar_lugar.html', {'lugar': lugar})

# Vista para modificar un lugar (solo para administradores)
@login_required
@user_passes_test(is_admin)
def modificar_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    ubicacion = lugar.ubicacion
    if request.method == 'POST':
        nuevo_numero = request.POST.get('nuevo_numero')
        if nuevo_numero:
            if Lugar.objects.filter(ubicacion=ubicacion, numero=nuevo_numero).exists():
                messages.error(request, 'Ya existe un lugar con este número en esta ubicación.')
            else:
                lugar.numero = nuevo_numero
                lugar.save()
                messages.success(request, 'Número de lugar actualizado exitosamente.')
                return redirect('lista_lugares', ubicacion_id=ubicacion.id)
        else:
            messages.error(request, 'El nuevo número de lugar no puede estar vacío.')
    return render(request, 'lugares/modificar_lugar.html', {'lugar': lugar, 'ubicacion': ubicacion})