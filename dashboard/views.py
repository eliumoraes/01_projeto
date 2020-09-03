from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import *

# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CreateUserForm
from django.contrib.auth.models import User

import re

import datetime

# class DricaPageView(TemplateView):
#     template_name = 'dri.html'

# Minhas Funções:
from .my_func import *
from .my_queries import *

    
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
    #data_tables = 'True'

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
        #'data_tables':data_tables, porque criei essa variável?
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
    categories = ClientCategory.objects.all()
    pagetitle = 'Dashboard'
    clients = dashClients()
    totais = len(ClientBackup.objects.all())
    pendentes = len(ClientBackup.objects.filter(status='P'))
    finalizados = len(ClientBackup.objects.filter(status='F'))
    assetscss = 'plugins/toastr/toastr.min.css'
    assetsjs = ('dist/js/client_copy.js,'
    +'plugins/toastr/toastr.min.js')

    context = {
        'menu':mainMenu(),
        'allClients':getClient(), 
        'pagetitle':pagetitle,
        'categories':categories,
        'clients': clients,
        'totais': totais,
        'pendentes': pendentes,
        'finalizados': finalizados,
        'assetscss': assetscss,
        'assetsjs': assetsjs
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
    client = str(client_id)
    categorie = str(client_cat)
    categories = ClientCategory.objects.all()
    categoryversions = CategoryVersion.objects.filter(category=categorie)
    clientProfile = getClient(categorie, client) # Relação entre cliente e categoria
    versions = getClientVersion(clientProfile, 1) # Passa a relação acima e recebe as versões
    backups = ClientBackup.objects.filter(client=clientProfile).order_by('-solic_date')
    ultima = getClientVersion(clientProfile, 2)
    finalizados = len(ClientBackup.objects.filter(status='F', client=clientProfile))
    totais = len(ClientBackup.objects.filter(client=clientProfile))
    cancelados = len(ClientBackup.objects.filter(status='C', client=clientProfile))

    # solic_pendente Usado na função do botão solicitar e atender
    # last_location usado para identificar o lugar onde está salvo
    try:
        if backups[0].status == 'P':
            last_location = (backups[1].destination.address 
            + backups[1].localizacao
            + ' : ' 
            + backups[1].destination.user
            + '@'
            + backups[1].destination.password
            
             )
            solic_pendente = True
        else:
            last_location = (backups[0].destination.address 
            + backups[0].localizacao
            + ' : ' 
            + backups[0].destination.user
            + '@'
            + backups[0].destination.password
            
             )

            solic_pendente = False
    except:
        solic_pendente = False
        last_location = 'Nenhum backup realizado!'


    if request.POST:
        print(request.POST)
        tipo = request.POST['tipo']
        print(tipo)
        print('acima tem que printar atualizacao...')

        if tipo == 'atualizacao':
            #Versao digitada/escolhida pelo usuário:
            capturedversion = (request.POST['new_version']).upper()

            #clientProfile vou associar com --> clientCat
            
            #usersave --> usuario
            usersave = User.objects.get(id=request.POST['user'])

            #versioncase --> version
            versioncase = CategoryVersion.objects.filter(category=categorie, version=capturedversion)

            #Verificar se a versão existe, então só tenho que associar.
            if len(versioncase)==1:
                print('A versão já existe...')
                #Caso sim, passar chave e salvar na relação com o cliente
                acerto = salvarVersao(clientProfile, versioncase[0], usersave)
                if not(acerto):
                    context = {
                        'menu':mainMenu(),
                        'pagetitle':'Erro', 
                        'message':'Já existe essa associação de versão.'
                        }
                    return render(request, 'error_01.html', context)
                else:
                    return redirect('clientupdate', client_id=client, client_cat=categorie)               
                
            elif len(versioncase)==0:
                #Caso não, criar a versão, passar chave e salvar na relação com o cliente
                CategoryVersion.objects.create(
                    category = ClientCategory.objects.get(id=categorie),
                    version = capturedversion
                )
                versioncase = CategoryVersion.objects.filter(category=categorie, version=capturedversion)
                acerto = salvarVersao(clientProfile, versioncase[0], usersave)
                if not(acerto):
                    context = {
                        'menu':mainMenu(),
                        'pagetitle':'Erro', 
                        'message':'Já existe essa associação de versão.'
                        }
                    return render(request, 'error_01.html', context)
                else:
                    return redirect('clientupdate', client_id=client, client_cat=categorie)

        
    # ultima = versions.reverse()[:1]
    pagetitle = clientProfile.client.name + ' ' + clientProfile.categorie.name

    # Meus CSS's
    assetscss = ('plugins/datatables-bs4/css/dataTables.bootstrap4.min.css,'
    +'plugins/datatables-responsive/css/responsive.bootstrap4.min.css,'
    +'plugins/select2/css/select2.min.css,'
    +'plugins/toastr/toastr.min.css,'
    +'dist/css/select-new.css')

    # Meus JS's
    assetsjs =('plugins/datatables/jquery.dataTables.min.js,' 
    +'plugins/datatables-bs4/js/dataTables.bootstrap4.min.js,'
    +'plugins/datatables-responsive/js/dataTables.responsive.min.js,'
    +'plugins/datatables-responsive/js/responsive.bootstrap4.min.js,'
    +'dist/js/data_tables_update.js,'
    +'dist/js/data_tables_backup.js,'
    +'dist/js/client_copy.js,'
    +'plugins/toastr/toastr.min.js,'
    +'plugins/select2/js/select2.full.min.js')

    catscript = ''
    for i in categoryversions:
        if(i != categoryversions[0]):
            catscript = catscript + ", '{}'".format(i.version)
        else:
            catscript = "'{}'".format(i.version)

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
        'client_id': client_id,
        'client_cat': client_cat,
        'versions':versions, 
        'backups':backups,
        'ultima':ultima,
        'script':script,
        'solic_pendente':solic_pendente,
        'last_location': last_location,
        'finalizados': finalizados,
        'totais': totais,
        'cancelados': cancelados
    }

    return render(request, 'client_view.html', context)


# -------------- PÁGINA P/ SOLICITAR BACKUP -------------- #
@login_required(login_url='login')
def backupRequest(request, client_id, client_cat, user_source):
    clientProfile = getClient(client_cat, client_id)
    pagetitle = clientProfile.client.name + ' / ' + clientProfile.categorie.name
    ultima = getClientVersion(clientProfile, 2)

    context = {
        #'assetscss':assetscss, 
        #'assetsjs':assetsjs,
        'menu':mainMenu(),
        'pagetitle': pagetitle,
        'client':"Cliente",
        #'ultima':"CP3.00.36",
        'clientProfile': clientProfile,
        'currentVersion': ultima
    }

    if (request.POST and request.POST['backup_request']=='requested'):
        print(request.POST)        
        client = getClient(request.POST['client_cat'], request.POST['client_id'])
        version = getClientVersion(clientProfile, 3, ultima)
        user = User.objects.get(id=request.POST['user'])
        save = saveBackupRequest(client, version, user)
        if not(save):
            context = {
                    'menu':mainMenu(),
                    'pagetitle':'Erro', 
                    'message':'Já existe a solicitação de backup para esta versão!'
                    }
            return render(request, 'error_01.html', context)
        else:
            if(user_source=='1'):
                return redirect('client', client_id=client_id, client_cat=client_cat)
            else:
                return redirect('home')



    return render(request, 'client_backup_request.html', context)

# -------------- PÁGINA PARA CRIAR LOCAIS DE ARMAZENAMENTO -------------- #
@login_required(login_url='login')
def storageNew(request):
    context = {
        #'assetscss':assetscss, 
        #'assetsjs':assetsjs,|
        'menu':mainMenu(),
        'pagetitle': "Criar local",
        'tipo': 'criar'
    }

    if (request.POST):
        print(request.POST)
        try:
            BackupDestination.objects.create(
                name= request.POST['storage_name'],
                user= request.POST['storage_user'],
                password= request.POST['storage_password'],
                address= request.POST['storage_address'],
                obs= request.POST['storage_obs']
            )
            return redirect('storage_list')
        except:
            print("Parece que deu erro...")

    return render(request, 'storage_create.html', context)

# -------------- PÁGINA PARA EDITAR LOCAIS DE ARMAZENAMENTO -------------- #
@login_required(login_url='login')
def storageEdit(request, storage_id):
    storage = BackupDestination.objects.get(id=storage_id)


    context = {
        #'assetscss':assetscss, 
        #'assetsjs':assetsjs,|
        'menu':mainMenu(),
        'pagetitle': "Editar local",
        'tipo': 'editar',
        'storage':storage
    }

    if (request.POST):
        print(request.POST)
        try:            
            storage.name= request.POST['storage_name']
            storage.user= request.POST['storage_user']
            storage.password= request.POST['storage_password']
            storage.address= request.POST['storage_address']
            storage.obs= request.POST['storage_obs']

            storage.save()
            
            return redirect('storage_list')
        except:
            print("Parece que deu erro...")

    return render(request, 'storage_create.html', context)

# -------------- FUNÇÃO DE ATIVAÇÃO/INATIVAÇÃO DE ARMAZENAMENTO -------------- #
@login_required(login_url='login')
def storageOnOff(request, storage_id, status):
    status = True if status=='True' else False
    storage = BackupDestination.objects.get(id=storage_id)
    try:
        if status:
            storage.status = False
        else:
            storage.status = True

        storage.save()
        return redirect('storage_list')
    except:
        print("Não conseguiu salvar")


        


# -------------- PÁGINA PARA LISTAR LOCAIS DE ARMAZENAMENTO -------------- #
@login_required(login_url='login')
def storageList(request):
    destinations = BackupDestination.objects.all()
    data_tables = 'True'

    # Meus CSS's
    assetscss = ('plugins/datatables-bs4/css/dataTables.bootstrap4.min.css,'
    +'plugins/datatables-responsive/css/responsive.bootstrap4.min.css'
    )

    # Meus JS's
    assetsjs =('plugins/datatables/jquery.dataTables.min.js,' 
    +'plugins/datatables-bs4/js/dataTables.bootstrap4.min.js,'
    +'plugins/datatables-responsive/js/dataTables.responsive.min.js,'
    +'plugins/datatables-responsive/js/responsive.bootstrap4.min.js,'
    +'dist/js/data_tables_storage_list.js'
    )

    context = {
        'assetscss':assetscss, 
        'assetsjs':assetsjs,
        'data_tables':data_tables,
        'menu': mainMenu(),
        'pagetitle': "Lista de locais",
        'destinations': destinations
    }


    return render(request, 'storage_list.html', context)

# -------------- PÁGINA PARA ATENDER SOLICITAÇÕES DE BACKUP -------------- #
@login_required(login_url='login')
def backupDelivery(request, client_id, client_cat, user_source, user_id):
    clientProfile = getClient(client_cat, client_id)
    pagetitle = clientProfile.client.name + ' / ' + clientProfile.categorie.name
    
    destinations = BackupDestination.objects.filter(status=True)

    # Meus CSS's
    assetscss = ('dist/css/select-new.css,'
    +'plugins/toastr/toastr.min.css')

    # Meus JS's:
    assestsjs = 'plugins/toastr/toastr.min.js'

    #status : mudar para finalizado
    #data : automatica

    context = {
        'menu': mainMenu(),
        'pagetitle': pagetitle,
        'destinations': destinations,
        'assetscss': assetscss,
        'assetsjs': assestsjs
    }


    if (request.POST):
        if request.POST['destination'] == 'Escolha uma das opções abaixo:':
            messages.warning(request, 'Você precisa escolher uma opção')
        else:
            print("Iniciar gravação", request.POST)
            date = request.POST['delivery_date'].split()
            date2 = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
            user = User.objects.get(id=request.POST['user'])
            dest = BackupDestination.objects.get(id=request.POST['destination'])
            location = request.POST['location']

            save = saveBackupDelivery(client=clientProfile, date=date2, user=user, destination=dest, location=location)
            if save:
                if(user_source=='1'):
                    return redirect('client', client_id=client_id, client_cat=client_cat)
                else:
                    return redirect('home')
            else:
                print("Renderizar página de erro...")
                context = {
                        'menu':mainMenu(),
                        'pagetitle':'Erro', 
                        'message':'Parece que deu erro! Tem que ver isso aí...'
                        }
                return render(request, 'error_01.html', context)



    return render(request, 'client_backup_delivery.html', context)

def servicesCreate(request):

    assetscss = ('dist/css/select-new.css')

    context = {
    'menu': mainMenu(),
    'pagetitle': 'Criar modelo de serviço',
    'assetscss': assetscss,
    # 'assetsjs': assestsjs
    }

    return render(request, 'services_create.html', context)