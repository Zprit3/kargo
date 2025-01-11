from django.urls import path
from .views import reservation_view, my_reservations, dashboard, reservation_success

urlpatterns = [
    path('reservation/', reservation_view, name='reservation'),
    path('my-reservations/', my_reservations, name='my_reservations'),
    path('dashboard/', dashboard, name='dashboard'),
    path('reservation/success/', reservation_success, name='reservation_success')


]