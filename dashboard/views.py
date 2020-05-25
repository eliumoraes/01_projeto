from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm
from django.contrib.auth.models import User

import re


# class DricaPageView(TemplateView):
#     template_name = 'dri.html'

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

                user = form.cleaned_data.get('username')
                messages.success(request, 'A conta ' + user +' foi criada com sucesso. Comunique o administrador para que seja aprovada.')
                return redirect('login')
        
        context ={'form':form}
        return render(request, 'register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
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
def approvedRegisterUser(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get('username')
            messages.success(request, 'Foi criada a conta para ' + user)
            return redirect('users')
    
    context ={
        'form':form, 
        'menu_admin':'True', 
        'menu_newuser':'True',
        'pagetitle':'Inserir novo usuário'
        }
    return render(request, 'register_approved.html', context)

@login_required(login_url='login')
def usersList(request):
    users = User.objects.all()
    data_tables = 'True'

    # Meus CSS's
    assetscss = ('plugins/datatables-bs4/css/dataTables.bootstrap4.min.css,'
    +'plugins/datatables-responsive/css/responsive.bootstrap4.min.css')

    # Meus JS's
    assetsjs =('plugins/datatables/jquery.dataTables.min.js,' 
    +'plugins/datatables-bs4/js/dataTables.bootstrap4.min.js,'
    +'plugins/datatables-responsive/js/dataTables.responsive.min.js,'
    +'plugins/datatables-responsive/js/responsive.bootstrap4.min.js,'
    +'dist/js/data_tables_language.js')

    context = {'users':users, 'assetscss':assetscss, 
    'assetsjs':assetsjs, 'menu_admin':'True', 
    'menu_userslist':'True', 
    'data_tables':data_tables,
    'pagetitle':'Lista de usuários'}
    return render(request, 'users_list.html', context)
    
@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def profilePage(request, user):
    userid = str(user)
    try:
        assetsjs = ('plugins/inputmask/min/jquery.inputmask.bundle.min.js,'
        +'dist/js/personal_masks.js')

        userprofile = UserProfile.objects.get(user__pk=userid)
        context = {'pagetitle':'Perfil', 'userprofile':userprofile, 'assetsjs':assetsjs}
        return render(request, 'profile.html', context)
    except:
        context = {'pagetitle':'Erro', 'message':'Parece que não foi encontrado um perfil para esse usuário.'}
        return render(request, 'error_01.html', context)

@login_required(login_url='login') 
def dricaTeste(request):
    clientes = Cliente.objects.all()
    context = {'clientes':clientes, 'pagetitle':'DricaTeste'}
    return render(request, 'dri.html', context)

@login_required(login_url='login') 
def homePage(request):
    clientes = Cliente.objects.all()
    pagetitle = 'Dashboard'

    context = {'clientes':clientes, 'pagetitle':pagetitle}
    return render(request, 'home.html', context)

@login_required(login_url='login')
def newClient(request):
    if request.POST:
        Cliente.objects.create(
            name = request.POST['client_name'],
            phone = re.sub('[^A-Za-z0-9]+', '', request.POST['client_phone']),
            email = request.POST['client_email']
        )

    assetsjs = ('plugins/inputmask/min/jquery.inputmask.bundle.min.js,'
    +'dist/js/personal_masks.js')

    context = {
        'pagetitle':'Novo cliente', 
        'assetsjs':assetsjs,
        'menu_clientes':'True',
        'menu_clientes_novo':'True',
        'menu_cadastros':'True'
    }
    return render(request, 'new_client.html', context)

@login_required(login_url='login')
def newClientCategory(request):
    if request.POST:
        ClientCategory.objects.create(
            name = request.POST['client_category_name'],
            icon = request.POST['client_category_icon']
        )

    context = {
        'menu_clientes':'True',
        'menu_cadastros':'True',
        'menu_clientes_novo_tipo': 'True',
        'pagetitle':'Categoria de cliente',
        
        }
    return render(request, 'new_client_category.html', context)