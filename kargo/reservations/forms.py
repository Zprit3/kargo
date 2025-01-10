from django import forms
from django.contrib.auth.models import User
from .models import Reservation, Client


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time']
    
    def save(self, commit=True):
        reservation = super().save(commit=False)
        if(commit):
            reservation.save()
            
            user, created = User.objects.get_or_create(
                username=self.cleaned_data['email'],
                defaults={'email': self.cleaned_data['email']}
            )
            if created:
                Client.objects.create(user=user, phone=self.cleaned_data['phone'], age = self.cleaned_data['age'])
        return reservation