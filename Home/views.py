from django.shortcuts import (
    render, redirect,
)
from django.contrib.auth import (
    authenticate, login, logout,
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def login_view(request):
    """ Login page, check for user login. """
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        except:
            print("[ERROR] Username or password is invalid")
            messages.error(request, "Username or password is invalid")
    
    return render(request, 'login.html')


def signup_view(request):
    """ Signup page, create a user. """
    return render(request, 'signup.html')


def logout_view(request):
    """ Logout user and redirect to index page. """
    logout(request)
    return redirect('/') 


def index_view(request):
    """ Index page. """
    return render(request, 'index.html')


@login_required(login_url='login')
def home_view(request):
    """ User home page. """
    return render(request, 'home.html')


@login_required(login_url='login')
def profil_view(request):
    """ User profil page. """
    return render(request, 'profil.html')


@login_required(login_url='login')
def myday_view(request):
    """ User daily results page. """
    return render(request, 'myday.html')