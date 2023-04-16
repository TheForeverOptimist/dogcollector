from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Dog
from django.views.generic import ListView

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'dogs/about.html')

def dogs_index(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', 
    {'dogs': dogs})

def dogs_detail(request, dog_id):
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})

class DogList(ListView):
    model = Dog

class DogCreate(CreateView):
    model = Dog
    fields = '__all__'
    success_url = '/dogs'
