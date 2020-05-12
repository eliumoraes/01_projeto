from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    
    #path('', HomePageView.as_view(), name='home'),
    #path('dri/', DricaPageView.as_view(), name='dri'),
    path('dri/', views.dricaTeste, name='dri'),

]
