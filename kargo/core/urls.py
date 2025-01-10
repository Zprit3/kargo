from django.urls import path
from .views import home, about_us, gallery

urlpatterns = [
    path('', home, name='home'),
    path('about/', about_us, name='about'),
    path('gallery/', gallery, name='gallery'),
]
