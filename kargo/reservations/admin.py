from django.contrib import admin
from .models import Client, Track, Reservation


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    list_display = ["user", "phone", "age"]


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):

    list_display = ["name", "track_type", "vehicle_count"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    list_display = ["client", "track", "date", "time", "status"]
