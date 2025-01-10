from django.shortcuts import render, redirect
from .models import Reservation, Track, Client
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
def reservation_view(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user.client #esto es asumiento que el cliente se vincula al usuario
            reservation.save()
            return redirect('my_reservations')
    else:
        form = ReservationForm()
    return render(request, 'reservation.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.object.filter(client=request.user.client)
    return render(request, 'my_reservations.html', {'reservations':reservations})

@login_required
def assign_track(request, reservation_id):
    reservation = Reservation.objects.get(id=reservation_id)
    available_tracks = Track.objects.filter(
        track_type=reservation.client.age_category,  # Define categorías según la edad
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
