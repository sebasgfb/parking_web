from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reserva, Lugar
from .forms import ReservaForm
from django.contrib import messages
from django.utils import timezone

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def detalle_lugar(request, lugar_id):
    lugar = get_object_or_404(Lugar, id=lugar_id)
    lugar.actualizar_estado()

    reservas = Reserva.objects.filter(lugar=lugar).order_by('fecha_reserva')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            nueva_reserva.lugar = lugar
            nueva_reserva.cliente = request.user

            # Validar fechas de reserva
            now = timezone.now()
            if nueva_reserva.fecha_reserva < now or nueva_reserva.fecha_liberacion < now:
                messages.error(request, "No se puede reservar en el pasado u hora actual.")
            elif nueva_reserva.fecha_reserva >= nueva_reserva.fecha_liberacion:
                messages.error(request, "La fecha de liberación debe ser posterior a la fecha de reserva.")
            else:
                # Verificar si hay reservas sobrepuestas
                conflicto = False
                for reserva in reservas:
                    if (nueva_reserva.fecha_reserva < reserva.fecha_liberacion and
                        nueva_reserva.fecha_liberacion > reserva.fecha_reserva):
                        conflicto = True
                        break

                if conflicto:
                    messages.error(request, "Ya existe una reserva en el intervalo de fechas seleccionadas.")
                else:
                    nueva_reserva.save()
                    messages.success(request, "Reserva creada exitosamente.")
                    return redirect('detalle_lugar', lugar_id=lugar.id)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ReservaForm()

    return render(request, 'reservas/detalle_lugar.html', {'lugar': lugar, 'reservas': reservas, 'form': form})


@login_required
@user_passes_test(is_admin)
def eliminar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    lugar_id = reserva.lugar.id
    if request.method == 'POST':
        reserva.delete()
        messages.success(request, "Reserva eliminada exitosamente.")
        return redirect('detalle_lugar', lugar_id=lugar_id)
    return render(request, 'reservas/eliminar_reserva.html', {'reserva': reserva})

@login_required
@user_passes_test(is_admin)
def modificar_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            
            # Validar fechas de reserva
            now = timezone.now()
            if nueva_reserva.fecha_reserva < now or nueva_reserva.fecha_liberacion < now:
                messages.error(request, "No se puede reservar en el pasado u hora actual.")
            elif nueva_reserva.fecha_reserva >= nueva_reserva.fecha_liberacion:
                messages.error(request, "La fecha de liberación debe ser posterior a la fecha de reserva.")
            else:
                # Verificar si hay reservas sobrepuestas
                conflicto = False
                otras_reservas = Reserva.objects.filter(lugar=reserva.lugar).exclude(id=reserva_id)
                for otra_reserva in otras_reservas:
                    if (nueva_reserva.fecha_reserva < otra_reserva.fecha_liberacion and
                        nueva_reserva.fecha_liberacion > otra_reserva.fecha_reserva):
                        conflicto = True
                        break

                if conflicto:
                    messages.error(request, "Ya existe una reserva en el intervalo de fechas seleccionadas.")
                else:
                    nueva_reserva.save()
                    messages.success(request, "Reserva modificada exitosamente.")
                    return redirect('detalle_lugar', lugar_id=reserva.lugar.id)
        else:
            messages.error(request, "Por favor corrige los errores en el formulario.")
    else:
        form = ReservaForm(instance=reserva)
    
    return render(request, 'reservas/modificar_reserva.html', {'form': form, 'reserva': reserva})