from django.shortcuts import render, redirect
from .models import Reservation, Track
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, "reservations/home.html")


def about_us(request):
    return render(request, "reservations/about_us.html")


def gallery(request):
    return render(request, 'reservations/gallery.html')


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