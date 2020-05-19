from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *

# class DricaPageView(TemplateView):
#     template_name = 'dri.html'

def dricaTeste(request):
    clientes = Cliente.objects.all()
    context = {'clientes':clientes}
    return render(request, 'dri.html', context)

def homePage(request):
    clientes = Cliente.objects.all()
    pagetitle = 'Dashboard'
    context = {'clientes':clientes, 'pagetitle':pagetitle}
    return render(request, 'home.html', context)