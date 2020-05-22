from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm
from django.contrib.auth.models import User


# class DricaPageView(TemplateView):
#     template_name = 'dri.html'

def registerUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            messages.success(request, 'Foi criada a conta para ' + user)
            return redirect('login')
    
    context ={'form':form}
    return render(request, 'register.html', context)


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Usuário ou Senha incorreta')

    context = {}
    return render(request, 'login.html', context)
    
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profilePage(request, user):
    userid = str(user)
    try:
        userprofile = UserProfile.objects.get(user__pk=userid)
        context = {'pagetitle':'Profile', 'userprofile':userprofile}
        return render(request, 'profile.html', context)
    except:
        context = {'pagetitle':'Erro', 'message':'Parece que não foi encontrado um perfil para esse usuário.'}
        return render(request, 'error_01.html', context)

@login_required(login_url='login') 
def dricaTeste(request):
    clientes = Cliente.objects.all()
    context = {'clientes':clientes}
    return render(request, 'dri.html', context)

@login_required(login_url='login') 
def homePage(request):
    clientes = Cliente.objects.all()
    pagetitle = 'Dashboard'

    context = {'clientes':clientes, 'pagetitle':pagetitle}
    return render(request, 'home.html', context)

