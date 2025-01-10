from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time']
        widget = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.Select(choices=[(f"{hour}:00", f"{hour}:00") for hour in range(8, 21)]),
        }