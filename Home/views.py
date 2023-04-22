from django.shortcuts import (
    render, redirect,
)
from django.contrib.auth import (
    authenticate, login, logout,
)
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Account
from Home.functions import (
    get_signup_form_fields, check_form_fields, create_account_using_form,
)


# Create your views here.


def error_view(request):
    """ Error page. """
    return render(request, 'error_page.html')


def login_view(request):
    """ Login page, check for user login. """
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            print("[ERROR] login : user does not exist")
            messages.error(request, "L'utilisateur n'existe pas.")
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "Le nom d'utilisateur ou le mot de passe est incorrect.")
        else:
            login(request, user)
            return redirect('home')

    return render(request, 'login.html')


def signup_view(request):
    """ Signup page, create a user. """
    gender = {
        "Homme": Account.Gender.MALE,
        "Femme": Account.Gender.FEMALE,
    }
    lifestyles = {
        "Aucune activité": Account.LifeStyle.ACTIVE_NONE,
        "Peu actif": Account.LifeStyle.ACTIVE_LOW,
        "Moyennement actif": Account.LifeStyle.ACTIVE_MED,
        "Très actif": Account.LifeStyle.ACTIVE_INT,
        "Professionnel": Account.LifeStyle.ACTIVE_PRO,
    }
    goals = {
        "Prendre du muscle": Account.GoalType.GAIN_WEIGHT,
        "Maintenir son poids": Account.GoalType.MAINTAIN_WEIGHT,
        "Perdre du poids": Account.GoalType.LOSE_WEIGHT,
    }
    context = {"gender": gender, "lifestyles": lifestyles, "goals": goals}

    if request.method == 'POST':
        # Recuperation des champs du formulaire
        form = get_signup_form_fields(request)
        check = check_form_fields(form)
        if check:
            # Verification si l'utilisateur existe deja en base de donnees
            if User.objects.filter(username=form.get('username'), email=form.get('email')).exists():
                print("[ERROR] signup : user does already exist")
                messages.error(request, "L'utilisateur existe déja, création du compte impossible.")
            # Creation du nouvel utilisateur en base de donnees
            else:
                account = create_account_using_form(form)
                account.save()
                print("[SUCCESS] signup : user was created")
                messages.success(request, "Votre compte à bien été créé !")
                return render(request, 'index.html')
        else:
            print("[ERROR] signup : invalid form fields")
            messages.error(request, "Des champs sont incorrects ou vides, veuillez saisir des informations valides.")
            return render(request, 'signup.html', context)

    return render(request, 'signup.html', context)


@login_required(login_url='/')
def logout_view(request):
    """ Logout user and redirect to index page. """
    logout(request)
    return redirect('/')


def index_view(request):
    """ Index page. """
    return render(request, 'index.html')


@login_required(login_url='/login/')
def home_view(request):
    """ User home page. """
    return render(request, 'home.html')


@login_required(login_url='/login/')
def progress_view(request):
    """ User progress page. """
    context = {}
    return render(request, 'progress.html', context)


@login_required(login_url='/login/')
def progress_add_view(request):
    """ User progress page. """
    context = {}
    if request.method == "POST":
        newWeight = int(request.POST.get("weight"))
        # TODO save in DB new weight => refactor weight storage in DB

    return render(request, 'progress.html', context)


@login_required(login_url='/login/')
def nutrition_view(request):
    """ User daily nutrition entries page. """
    return render(request, 'nutrition.html')


@login_required(login_url='/login/')
def activity_view(request):
    """ User daily activity entries page. """
    return render(request, 'activity.html')


@login_required(login_url='/login/')
def training_view(request):
    """ Training guides page. """
    return render(request, 'training.html')


@login_required(login_url='/login/')
def community_view(request):
    """ Community page. """
    return render(request, 'community.html')


@login_required(login_url='/login/')
def parameters_view(request):
    """ User parameters page. """
    context = {}
    if (request.user != User.objects.get(username='admin')):
        current_user = User.objects.get(id=request.user.id)
        account = Account.objects.get(user=current_user)
        context = {"account": account}
    return render(request, 'parameters.html', context)
