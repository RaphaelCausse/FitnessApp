from django.contrib import messages
from django.contrib.auth.models import User
from .models import Account
from datetime import date


def get_signup_form_fields(request):
    """ Get signup form fields and return a dictionary. """
    firstname = request.POST.get('firstname', None)
    lastname = request.POST.get('lastname')
    birthdate = request.POST.get('birthdate', None)
    gender = request.POST.get('gender', None)
    username = request.POST.get('username', None)
    email = request.POST.get('email', None)
    password = request.POST.get('password', None)
    confirm_password = request.POST.get('confirm_password', None)
    weight = request.POST.get('weight', None)
    height = request.POST.get('height', None)
    lifestyle = request.POST.get('lifestyle', None)
    goal = request.POST.get('goal', None)
    goal_weight = request.POST.get('goal_weight', None)

    form = {
        "firstname": firstname,
        "lastname": lastname,
        "birthdate": birthdate,
        "gender": gender,
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": confirm_password,
        "weight": weight,
        "height": height,
        "lifestyle": lifestyle,
        "goal": goal,
        "goal_weight": goal_weight,
    }
    return form


def check_form_fields(form):
    """ Check if form fields are not None. """
    is_valid = True
    for key, val in form.items():
        if val == None:
            is_valid = False
    return is_valid


def create_account_using_form(form):
    """ Create an Account using form fields. """
    user = User.objects.create_user(
        username=form.get('username'),
        email=form.get('email'),
        password=form.get('password'),
    )
    user.first_name = form.get('firstname'),
    user.last_name = form.get('lastname')
    user.save()
    birthdate = form.get('birthdate').split("-")
    account = Account.objects.create(
        user=user,
        birthdate=date(
            int(birthdate[0]), int(birthdate[1]), int(birthdate[2])
        ),
        gender=form.get('gender'),
        weight=form.get('weight'),
        height=form.get('height'),
        lifestyle=form.get('lifestyle'),
        goalType=form.get('goal'),
        goalWeight=form.get('goal_weight'),
        results=None,
    )
    return account
