from django.shortcuts import (
    render, redirect,
)
from django.contrib.auth import (
    authenticate, login, logout,
)
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import (
    Result, Account, SocialPost, LikedPost, DislikedPost, Meal, Food,
)
from Home.functions import (
    get_signup_form_fields, check_form_fields, create_account_using_form,
)
import datetime as dt
from . import helpers
import json


# Create your views here.

def login_view(request):
    """ Login page, check for user login. """
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except:
            print(f"[ERROR] login : user '{username}' does not exist")
            messages.error(request, "L'utilisateur n'existe pas. Réessayez.")
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
                print(f"[ERROR] signup : user '{form.get('username')}' does already exist")
                messages.error(request, "L'utilisateur existe déja, création du compte impossible.")
            # Creation du nouvel utilisateur en base de donnees
            else:
                account = create_account_using_form(form)
                account.save()
                print(f"[SUCCESS] signup : user '{form.get('username')}' was created")
                messages.success(request, "Votre compte à bien été créé !")
                return render(request, 'index.html')
        else:
            print("[ERROR] signup : invalid form fields")
            messages.error(request, "Des champs sont incorrects ou vides, veuillez saisir des informations valides.")

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
    context = {}

    current_user = User.objects.get(id=request.user.id)
    account = Account.objects.get(user=current_user)

    # TODO Recup les calories du jour de Food, les calories du jour de Activity
    day_food_calories = 1250  # TODO
    day_activity_calories = 50  # TODO
    # TODO Moyenne de calories journalieres des 15 derniers jours
    average_calories = 50  # TODO

    context = {
        "goal_calories": account.goalCalories,
        "day_food_calories": day_food_calories,
        "day_activity_calories": day_activity_calories,
        "average_calories": average_calories,
    }
    return render(request, 'home.html', context)


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
        current_user = User.objects.get(id=request.user.id)
        account = Account.objects.get(user=current_user)
        new_weight = int(request.POST.get("weight"))

        try:
            # Modification du poids dans les resultats du jour
            result_of_day = Result.objects.get(date=dt.date.today(), owner=account)
            result_of_day.weight = new_weight
            result_of_day.save()
            print(result_of_day)
        except:
            # Creation d'un resultat du jour.
            new_result = Result.objects.create(weight=new_weight, owner=account)
            print(new_result)

    return render(request, 'progress.html', context)


@login_required(login_url='/login/')
def nutrition_view(request):
    """ User daily nutrition entries page. """
    context = helpers.get_calories_of_the_day(request)
    account = Account.objects.get(user=request.user)
    context.update({"calories_goal": account.goalCalories})
    return render(request, 'nutrition.html', context)


@login_required(login_url='/login/')
def activity_view(request):
    """ User daily activity entries page. """
    user = User.objects.get(id=request.user.id)
    context = helpers.get_activities_of_the_week(user)
    return render(request, 'activity.html', context)


@login_required(login_url='/login/')
def training_view(request):
    """ Training guides page. """
    return render(request, 'training.html')


@login_required(login_url='/login/')
def social_view(request):
    """ Social page with social posts. """
    posts = SocialPost.objects.all()
    current_user = User.objects.get(id=request.user.id)
    account = Account.objects.get(user=current_user)
    liked_posts = [lp.post.id for lp in LikedPost.objects.filter(liker=account)]
    disliked_posts = [dp.post.id for dp in DislikedPost.objects.filter(disliker=account)]
    context = {"account": account, "posts": posts, "liked": liked_posts, "disliked": disliked_posts}
    return render(request, 'social.html', context)


@login_required(login_url='/login/')
def social_add_view(request):
    """ Add a social post. """
    if request.method == "POST":
        current_user = User.objects.get(id=request.user.id)
        account = Account.objects.get(user=current_user)
        newPost = SocialPost.objects.create(
            author=account,
            text=request.POST.get('message'),
            likes=0,
            dislikes=0,
        )
        newPost.save()
    return redirect('/social')


@csrf_exempt
@login_required(login_url='/login/')
def social_update_ajax_view(request):
    response = {}
    if request.method == "POST":
        # Recuperation de la requete ajax
        ajax_request = {key: int(value) for (key, value) in request.POST.items()}
        # Recuperer en BDD les objets concernes
        current_user = User.objects.get(id=request.user.id)
        account = Account.objects.get(user=current_user)
        postId = ajax_request.get("post_id")
        socialPost = SocialPost.objects.get(id=postId)

        # Faire les modifications sur la base de donnees
        likes = ajax_request.get("likes")
        dislikes = ajax_request.get("dislikes")

        # Si le post a ete like, ajout a la table LikedPost
        if likes > socialPost.likes:
            socialPost.likes += 1
            to_add = LikedPost.objects.create(
                liker=account,
                post=socialPost
            )
            to_add.save()
            socialPost.save()
        # Si le post n'est plus like, supression de la table LikedPost
        if likes < socialPost.likes:
            socialPost.likes -= 1
            to_rem = LikedPost.objects.get(liker=account, post=socialPost)
            to_rem.delete()
            socialPost.save()

        # Si le post a ete dislike, ajout a la table DislikedPost
        if dislikes > socialPost.dislikes:
            socialPost.dislikes += 1
            to_add = DislikedPost.objects.create(
                disliker=account,
                post=socialPost
            )
            to_add.save()
            socialPost.save()
        # Si le post n'est plus dislike, suppression de la table DislikedPost
        if dislikes < socialPost.dislikes:
            socialPost.dislikes -= 1
            to_rem = DislikedPost.objects.get(disliker=account, post=socialPost)
            to_rem.delete()
            socialPost.save()

    return JsonResponse(response)


@login_required(login_url='/login/')
def social_delete_view(request, id):
    """ Delete a specific social post. """
    post = SocialPost.objects.get(id=id)

    if request.method == "POST":
        post.delete()
        return redirect('/social')

    context = {"post": post}
    return render(request, 'social_delete.html', context)


@login_required(login_url='/login/')
def parameters_view(request):
    """ User parameters page. """
    context = {}
    if (request.user != User.objects.get(username='admin')):
        current_user = User.objects.get(id=request.user.id)
        account = Account.objects.get(user=current_user)
        age = account.get_age()
        context = {"account": account, "age": age}
    return render(request, 'parameters.html', context)


@csrf_exempt
def autocomplete(request):
    if request.method == "POST":
        pattern = request.POST.get('product')
        products = helpers.autocomplete_products(pattern)
        return JsonResponse({"products": products}, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=False)


@csrf_exempt
def search_product(request):
    if request.method == "POST":
        product = request.POST.get('product')
        product_index = int(request.POST.get('product-index'))
        product_data = helpers.search_product(product, product_index)
        return JsonResponse(product_data, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=False)


@csrf_exempt
def add_product_to_db(request):
    if request.method == "POST":
        data = request.POST
        helpers.add_product_to_db(data)
        return JsonResponse({"success": "Product added"}, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=False)


@csrf_exempt
def add_product_to_user(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.get(id=request.user.id)
        helpers.add_product_to_user(user, data)
        context = helpers.get_calories_of_the_day(request)
        return JsonResponse(context, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=False)


@csrf_exempt
def add_activity_to_user(request):
    if request.method == "POST":
        data = request.POST
        user = User.objects.get(id=request.user.id)
        helpers.add_activity_to_user(user, data)
        context = helpers.get_activities_of_the_week(user)
        return JsonResponse(context, status=200, safe=False)
    return JsonResponse({"error": ""}, status=400, safe=False)
