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

def mainMenu():
    clientCategory = ClientCategory.objects.all()
    listaMaior = []
    listaMenor = []
    for cat in clientCategory:
        listaMenor = [[cat.name, cat.icon]]
        listaMenor.extend(ClientCategoryRelation.objects.filter(categorie=cat))
        listaMaior.append(listaMenor)
    
    listaMaior.sort()
    return listaMaior

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
def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def approvedRegisterUser(request):
    form = CreateUserForm()
    categories = ClientCategory.objects.all()

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
        'pagetitle':'Inserir novo usuário',
        'categories':categories,
        'menu':mainMenu(),
        }
    return render(request, 'register_approved.html', context)

@login_required(login_url='login')
def usersList(request):
    users = User.objects.all()
    categories = ClientCategory.objects.all()
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

    context = {
        'users':users, 
        'assetscss':assetscss, 
        'assetsjs':assetsjs, 
        'menu_admin':'True', 
        'menu_userslist':'True', 
        'data_tables':data_tables,
        'pagetitle':'Lista de usuários',
        'categories':categories,
        'menu':mainMenu(),
    }
    return render(request, 'users_list.html', context)


@login_required(login_url='login')
def profilePage(request, user):
    userid = str(user)
    categories = ClientCategory.objects.all()

    try:
        assetsjs = ('plugins/inputmask/min/jquery.inputmask.bundle.min.js,'
        +'dist/js/personal_masks.js')

        userprofile = UserProfile.objects.get(user__pk=userid)
        context = {
            'menu':mainMenu(),
            'pagetitle':'Perfil', 
            'userprofile':userprofile, 
            'assetsjs':assetsjs,
            'categories':categories
            }
        return render(request, 'profile.html', context)
    except:
        context = {
            'menu':mainMenu(),
            'pagetitle':'Erro', 
            'message':'Parece que não foi encontrado um perfil para esse usuário.',
            'categories':categories}
        return render(request, 'error_01.html', context)

@login_required(login_url='login') 
def dricaTeste(request):
    categories = ClientCategory.objects.all()
    clientes = Cliente.objects.all()
    context = {
        'menu':mainMenu(),
        'clientes':clientes, 
        'pagetitle':'DricaTeste',
        'categories':categories,
        }
    return render(request, 'dri.html', context)

@login_required(login_url='login') 
def homePage(request):
    clientes = Cliente.objects.all()
    categories = ClientCategory.objects.all()
    pagetitle = 'Dashboard'

    context = {
        'menu':mainMenu(),
        'clientes':clientes, 
        'pagetitle':pagetitle,
        'categories':categories,
        }
    return render(request, 'home.html', context)

# -------------- VIEW PARA CADASTRO DE CLIENTE -------------- #
@login_required(login_url='login')
def newClient(request):
    clientes = Cliente.objects.all()
    listaClientes = []
    for item in clientes:
        listaClientes.append(item.name)

    categories = ClientCategory.objects.all()

    if request.POST:
        print(request.POST)
        namein = (' '.join((request.POST['client_name']).split())).title()
        phonein = re.sub('[^A-Za-z0-9]+', '', request.POST['client_phone'])
        emailin = request.POST['client_email']
        categoriain = int(request.POST['client_type'])
        
        print(type(categoriain))

        print(namein + ' ' +phonein + ' ' +emailin +' ' +str(categoriain))

        cat = ClientCategory.objects.get(id=categoriain)
        criaCliente = Cliente.objects.filter(name=namein)

        # """ Iniciando rotina para criação de cliente: """

        # Verifica se o cliente existe:
        if( len(criaCliente) == 1 ):
            print('Len é igual a 1')
            #Se existe:
            #Verifica se está registrado no sistema indicado
            if ClientCategoryRelation.objects.filter(categorie=cat, client=criaCliente[0]).exists():
                print('Já existe o registro')
                #Se estiver registrado informa que o cliente / registro já existe
                #Aqui eu posso passar uma página de erro, porém devo mudar a chamada para uma classe
                context = {
                'menu':mainMenu(),
                'pagetitle':'Erro', 
                'message':'O cliente informado já possui registro na categoria indicada.'
                }
                return render(request, 'error_01.html', context)  
            else:
                print('Pode gravar com tranquilidade')
                #Se não estiver efetua o registro
                insereClienteNaCategoria = ClientCategoryRelation(categorie=cat, client=criaCliente[0])
                insereClienteNaCategoria.save()
                print(insereClienteNaCategoria)

        elif( len(criaCliente) > 1):
            context = {
            'menu':mainMenu(),
            'pagetitle':'Erro', 
            'message':'Existem 2 ou mais clientes com o mesmo nome.'
            }
            return render(request, 'error_01.html', context)            
        else:
            # Se não existe:
            # Cria o cliente
            print('Esse cliente ainda não existe')
            Cliente.objects.create(
                name = (' '.join((request.POST['client_name']).split())).title(),
                phone = re.sub('[^A-Za-z0-9]+', '', request.POST['client_phone']),
                email = request.POST['client_email']
            )
            # Efetua o registro            
            criaCliente = Cliente.objects.filter(name=namein)
            insereClienteNaCategoria = ClientCategoryRelation(categorie=cat, client=criaCliente[0])
            insereClienteNaCategoria.save()
            print(insereClienteNaCategoria)
       

    assetsjs = ('plugins/inputmask/min/jquery.inputmask.bundle.min.js,'
                +'dist/js/personal_masks.js,'
                +'plugins/select2/js/select2.full.min.js')

    assetscss = ('plugins/select2/css/select2.min.css,'
                +'dist/css/select-new.css')

    cliscript = ''
    for i in clientes:
        if(i != clientes[0]):
            cliscript = cliscript + ", '{}'".format(i)
        else:
            cliscript = "'{}'".format(i)

    script = ("""
<script>
    $(document).ready(function() {

    //Initialize Select2 Elements
    $('.select2').select2({
      theme: 'bootstrap4'
    });

    var clientslist = [""" +cliscript +"""];
    $('.select2').select2({
        data: clientslist,
        tags: true
    });
    });
</script>
        """)

    context = {
        'menu':mainMenu(),
        'pagetitle':'Novo cliente', 
        'assetsjs':assetsjs,
        'assetscss':assetscss,
        'menu_clientes':'True',
        'menu_clientes_novo':'True',
        'menu_cadastros':'True',
        'script':script,
        'categories':categories,
    }
    return render(request, 'new_client.html', context)

# -------------- VIEW PARA REGISTRO DE CATEGORIA -------------- #
@login_required(login_url='login')
def newClientCategory(request):
    categories = ClientCategory.objects.all()
    if request.POST:
        ClientCategory.objects.create(
            name = request.POST['client_category_name'],
            icon = request.POST['client_category_icon']
        )

    context = {
        'menu':mainMenu(),
        'menu_clientes':'True',
        'menu_cadastros':'True',
        'menu_clientes_novo_tipo': 'True',
        'pagetitle':'Categoria de cliente',
        'categories':categories
        }
    return render(request, 'new_client_category.html', context)

# -------------- PÁGINA DO CLIENTE -------------- #
@login_required(login_url='login')
def clientPage(request, client_id, client_cat):
    cliente = str(client_id)
    categorie = str(client_cat)
    categories = ClientCategory.objects.all()
    categoryversions = CategoryVersion.objects.filter(category=categorie)
    clientProfile = ClientCategoryRelation.objects.get(categorie__pk=categorie, client__pk=cliente)
    versions = ClientCategoryVersion.objects.filter(clientCat=clientProfile).order_by('-dataHora')
    if(len(versions) == 0):
        ultima = 'Informar!'
    else:
        ultima = (versions[:1])[0].version.version
        
    # ultima = versions.reverse()[:1]
    pagetitle = clientProfile.client.name + ' ' + clientProfile.categorie.name

    # Meus CSS's
    assetscss = ('plugins/datatables-bs4/css/dataTables.bootstrap4.min.css,'
    +'plugins/datatables-responsive/css/responsive.bootstrap4.min.css,'
    +'plugins/select2/css/select2.min.css,'
    +'dist/css/select-new.css')

    # Meus JS's
    assetsjs =('plugins/datatables/jquery.dataTables.min.js,' 
    +'plugins/datatables-bs4/js/dataTables.bootstrap4.min.js,'
    +'plugins/datatables-responsive/js/dataTables.responsive.min.js,'
    +'plugins/datatables-responsive/js/responsive.bootstrap4.min.js,'
    +'dist/js/data_tables_language.js,'
    +'plugins/select2/js/select2.full.min.js')

    catscript = ''
    for i in categoryversions:
        if(i != categoryversions[0]):
            catscript = catscript + ", '{}'".format(i)
        else:
            catscript = "'{}'".format(i)

    script = ("""
<script>
    $(document).ready(function() {

    //Initialize Select2 Elements
    $('.select2').select2({
      theme: 'bootstrap4'
    });

    var clientslist = [""" +catscript +"""];
    $('.select2').select2({
        data: clientslist,
        tags: true
    });
    });
</script>
        """)

    context = {
        'assetscss':assetscss, 
        'assetsjs':assetsjs,
        'menu':mainMenu(),
        'categories':categories,
        'pagetitle':pagetitle,
        'clientProfile':clientProfile,
        'versions':versions,
        'ultima':ultima,
        'script':catscript
    }

    return render(request, 'client_view.html', context)