from django.urls import path
from .views import reservation_view, my_reservations, dashboard

urlpatterns = [
    path('reservation/', reservation_view, name='reservation'),
    path('my-reservations/', my_reservations, name='my_reservations'),
    path('dashboard/', dashboard, name='dashboard')

]