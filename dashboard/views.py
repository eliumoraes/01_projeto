from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *

class HomePageView(TemplateView):
    template_name = 'home.html'

class DricaPageView(TemplateView):
    template_name = 'dri.html'

def dricaTeste(request):
    clientes = Cliente.objects.all()
    context = {'clientes':clientes}
    return render(request, 'dri.html', context)