from django.shortcuts import render, redirect

def home(request):
    return render(request, "core/home.html")


def about_us(request):
    return render(request, "core/about_us.html")


def gallery(request):
    return render(request, 'core/gallery.html')
