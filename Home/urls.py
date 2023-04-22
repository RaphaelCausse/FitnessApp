from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('error', views.error_view, name='error'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('progress/', views.progress_view, name='progress'),
    path('progress/add', views.progress_add_view, name='progress_add'),
    path('nutrition/', views.nutrition_view, name='nutrition'),
    path('activity/', views.activity_view, name='activity'),
    path('training/', views.training_view, name='training'),
    path('community/', views.community_view, name='community'),
    path('parameters/', views.parameters_view, name='parameters'),
]
