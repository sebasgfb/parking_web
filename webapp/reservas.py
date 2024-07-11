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
    reservas = Reserva.objects.filter(lugar=lugar).order_by('fecha_reserva')  # Ordenar las reservas por fecha_reserva

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            nueva_reserva = form.save(commit=False)
            nueva_reserva.lugar = lugar
            nueva_reserva.cliente = request.user

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
