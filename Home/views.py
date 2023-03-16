from django.shortcuts import render
from .models import Account
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    """ Render index page (when user is not connected). """
    return render(request, 'index.html')


def home(request):
    """ Render home page (when user is connected). """
    user = User(username="Thomas")
    account = Account(user=user)
    context = {"account": account}
    return render(request, 'home.html', context)
