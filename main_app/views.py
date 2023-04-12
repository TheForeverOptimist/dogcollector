from django.shortcuts import render

#baby step usually a model willbe used
dogs = [
    {'name': 'Lolo', 'breed': 'spaniel', 'description': 'cutest', 'age': 3},
    {'name': 'Cash', 'breed': 'shitzu', 'description': 'fiesty', 'age': 1},
]

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def index(request):
    return render(request, 'index.html', {
        'dogs': dogs
    })
