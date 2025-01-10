from django.urls import path
from .views import home, about_us, gallery, reservation_view, my_reservations

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_us, name='about'),
    path('gallery/', gallery, name='gallery'),
    path('reservation/', reservation_view, name='reservation'),
    path('my-reservations/', my_reservations, name='my_reservations')
    
]