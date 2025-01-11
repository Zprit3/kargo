from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Reservation, Track, Client
from .forms import ReservationForm, VisitorReservationForm

def reservation_view(request):
    if request.user.is_authenticated:
        # Usuario autenticado: usa el formulario simplificado
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                reservation = form.save(commit=False)
                reservation.client = request.user.client  # Vincula al cliente existente
                reservation.save()
                messages.success(request, "Reserva creada con éxito.")
                return redirect('my_reservations')
        else:
            form = ReservationForm()
        return render(request, 'reservations/reservation.html', {'form': form, 'authenticated': True})
    
    else:
        # Usuario no autenticado: usa el formulario que incluye datos del cliente
        if request.method == "POST":
            form = VisitorReservationForm(request.POST)
            if form.is_valid():
                # Crear o usar cliente existente
                email = form.cleaned_data['email']
                user, created = User.objects.get_or_create(
                    username=email, defaults={'email': email}
                )
                if created:
                    client = Client.objects.create(
                        user=user,
                        phone=form.cleaned_data['phone'],
                        age=form.cleaned_data['age']
                    )
                else:
                    client = user.client

                # Guardar reserva
                reservation = form.save(commit=False)
                reservation.client = client
                reservation.save()
                messages.success(request, "Reserva creada con éxito.")
                return redirect('reservation_success')  # Redirige a una página de éxito
        else:
            form = VisitorReservationForm()
        return render(request, 'reservations/reservation.html', {'form': form, 'authenticated': False})


@login_required
def dashboard(request):
    reservations = Reservation.objects.all()
    tracks = Track.objects.all()
    clients = Client.objects.all()
    
    context = {
        'reservations': reservations,
        'tracks': tracks,
        'clients': clients,
    }
    return render(request, 'reservations/dashboard.html', context)


@login_required
def my_reservations(request):
    try:
        client = request.user.client  # Intenta obtener el cliente asociado al usuario
    except Client.DoesNotExist:
        messages.error(request, "No se encontró un cliente asociado a este usuario. Por favor, contáctese con soporte.")
        return redirect('reservation')  # Redirige a la página de reservas

    reservations = Reservation.objects.filter(client=client)
    return render(request, 'reservations/my_reservations.html', {'reservations': reservations})


@login_required
def assign_track(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    available_tracks = Track.objects.filter(
        track_type=reservation.client.age_category,
        reservation__date=reservation.date,
        reservation__time=reservation.time
    )
    if available_tracks.exists():
        reservation.track = available_tracks.first()
        reservation.status = 'reserved'
        reservation.save()
        messages.success(request, "Track assigned successfully!")
        return redirect('dashboard')
    else:
        messages.error(request, "No tracks available at this time.")
    return redirect('reservation_list')


def reservation_success(request):
    return render(request, 'reservations/success.html')