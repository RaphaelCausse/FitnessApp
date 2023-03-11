from django.shortcuts import render

# Create your views here.

def index(request):
    """ Render index page (when user is not connected). """
    return render(request, 'index.html')

def home(request):
    """ Render home page (when user is connected). """
    return render(request, 'home.html')