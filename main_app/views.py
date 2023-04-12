from django.shortcuts import render
from .models import Dog

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'dogs/about.html')

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', 
    {'dogs': dogs})
