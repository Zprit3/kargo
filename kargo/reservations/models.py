from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    age = models.PositiveIntegerField()
    
    def __str__(self):
        return self.user.username

class Track(models.Model):
    TRACK_TYPES = (
        ('children', 'Children'),
        ('youth', 'Youth'),
        ('adults', 'Adults'),
    )
    
    name = models.CharField(max_length=100)
    track_type = models.CharField(max_length=10, choices=TRACK_TYPES)
    vehicle_count = models.PositiveIntegerField()
    
    class Meta:
        permissions = [
            ("can_manage_tracks", "Can manage tracks"),
            ("can_view_reservations", "Can view reservations")
        ]
    
    def __str__(self):
        return self.name
    
    
class Reservation(models.Model):
    STATUS_CHOICES = (
        ('reserved','Reserved'),
        ('occupied','Ocuppied'),
        ('released','Released'),
        ('finished','Finished'),
    )
    
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, null=True, on_delete=models.SET_NULL)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='reserved')
    
    def __str__(self):
        return f"{self.client} - {self.track} on {self.date} at {self.time}"