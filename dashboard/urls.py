from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    
    path('', views.homePage, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('register2', views.approvedRegisterUser, name='register2'),
    path('profile/<str:user>/', views.profilePage, name='profile'),
    path('dri/', views.dricaTeste, name='dri'),
    path('users/', views.usersList, name='users'),
    path('new_client/', views.newClient, name='new_client'),
    path('new_client_category/', views.newClientCategory, name='new_client_category'),
    path('client/<str:client_id>/<str:client_cat>/', views.clientPage, name='client')

] 
