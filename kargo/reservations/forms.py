from django import forms
from .models import Client, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class ReservationForm(forms.ModelForm):
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    age = forms.IntegerField(required=False)
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        help_text="Ingrese una contraseña si desea crear una cuenta"
    )

    class Meta:
        model = Reservation
        fields = ['date', 'time']

    def save(self, commit=True):
        reservation = super().save(commit=False)
        if commit:
            reservation.save()

            # Si el usuario no está autenticado, creamos uno nuevo
            if not self.cleaned_data.get('email') or not self.cleaned_data.get('password'):
                return reservation  # Usuario logueado, no hacemos nada adicional
            
            user, created = User.objects.get_or_create(
                username=self.cleaned_data['email'],
                defaults={
                    'email': self.cleaned_data['email'],
                    'password': make_password(self.cleaned_data['password'])
                }
            )
            if created:
                Client.objects.create(
                    user=user,
                    phone=self.cleaned_data['phone'],
                    age=self.cleaned_data['age']
                )
        return reservation

class VisitorReservationForm(forms.ModelForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    age = forms.IntegerField()

    class Meta:
        model = Reservation
        fields = ['date', 'time', 'email', 'phone', 'age']
