import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dog, Toy, Photo
from .forms import FeedingForm

# Create your views here.
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'dogs/about.html')

@login_required
def dogs_index(request):
  dogs = Dog.objects.filter(user=request.user)
  # Another query
  # dogs = request.user.cat_set.all()
  return render(request, 'dogs/index.html', {
    'dogs': dogs
  })
@login_required
def dogs_detail(request, dog_id):
  dog = Dog.objects.get(id=dog_id)

  id_list = dog.toys.all().values_list('id')

  toys_dog_doesnt_have = Toy.objects.exclude(id__in=id_list)

  feeding_form = FeedingForm()
  return render(request, 'dogs/detail.html', {
    'dog': dog, 'feeding_form': feeding_form,
    'toys': toys_dog_doesnt_have
  })
class DogCreate(LoginRequiredMixin, CreateView):
  model = Dog
  fields = ['name', 'breed', 'description', 'age']
  def form_valid(self, form):
  
    form.instance.user = self.request.user

    return super().form_valid(form)
  
class DogUpdate(LoginRequiredMixin, UpdateView):
  model = Dog
  fields = ['breed', 'description', 'age']

class DogDelete(LoginRequiredMixin, DeleteView):
  model = Dog
  success_url = '/dogs'


@login_required
def add_feeding(request, dog_id):
  # create a ModelForm instance using
  # the data that was submitted in the form
  form = FeedingForm(request.POST)
  # validate the form
  if form.is_valid():
    # We want a model instance, but
    # we can't save to the db yet
    # because we have not assigned the
    # dog_id FK.
    new_feeding = form.save(commit=False)
    new_feeding.dog_id = dog_id
    new_feeding.save()
  return redirect('detail', dog_id=dog_id)

class ToyList(LoginRequiredMixin, ListView):
  model = Toy


class ToyDetail(LoginRequiredMixin, DetailView):
  model = Toy

class ToyCreate(LoginRequiredMixin, CreateView):
  model = Toy
  fields = '__all__'

class ToyUpdate(LoginRequiredMixin, UpdateView):
  model = Toy
  fields = ['name', 'color']

class ToyDelete(LoginRequiredMixin, DeleteView):
  model = Toy
  success_url = '/toys'

@login_required
def assoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.add(toy_id)
  return redirect('detail', dog_id=dog_id)

@login_required
def unassoc_toy(request, dog_id, toy_id):
  Dog.objects.get(id=dog_id).toys.remove(toy_id)
  return redirect('detail', dog_id=dog_id)

@login_required
def add_photo(request, dog_id):
  # photo-file maps to the "name" attr on the <input>
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    # Need a unique "key" (filename)
    # It needs to keep the same file extension
    # of the file that was uploaded (.png, .jpeg, etc.)
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
    try:
      bucket = os.environ['S3_BUCKET']
      s3.upload_fileobj(photo_file, bucket, key)
      url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
      Photo.objects.create(url=url, dog_id=dog_id)
    except Exception as e:
      print('An error occurred uploading file to S3')
      print(e)
  return redirect('detail', dog_id=dog_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # Save the user to the db
      user = form.save()
      # Automatically log in the new user
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup template
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)














