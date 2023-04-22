from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('progress/', views.progress_view, name='progress'),
    path('nutrition/', views.nutrition_view, name='nutrition'),
    path('activity/', views.activity_view, name='activity'),
    path('training/', views.training_view, name='training'),
    path('social/', views.social_view, name='social'),
    path('social/add/', views.social_add_view, name='social_add'),
    path('social/update/', views.social_update_ajax_view, name='social_update'),
    path('social/delete/<str:id>', views.social_delete_view, name='social_delete'),
    path('parameters/', views.parameters_view, name='parameters'),
]
