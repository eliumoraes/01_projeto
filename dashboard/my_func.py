from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def getClient(categorie='all', client='all'):
    if (categorie=='all' and client=='all'):
        return ClientCategoryRelation.objects.all().order_by('client__name', 'categorie__name')
    else:
        return ClientCategoryRelation.objects.get(categorie__pk=categorie, client__pk=client)

def getClientVersion(clientProfile, check, version=''):
    # Receber variável que indica se quer todas as versões, ou somente a última, ou versão única (padrão para gravação)
    allVersions = ClientCategoryVersion.objects.filter(clientCat=clientProfile).order_by('-dataHora')
    if check==1:
        return allVersions
    elif check==2:
        if(len(allVersions) == 0):
            return 'Informar!'
        else:
            return (allVersions[:1])[0].version.version
    else:
        return ClientCategoryVersion.objects.get(clientCat=clientProfile, version__version=version)

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

def salvarVersao(clientcat, version, usuario):
    #Verificar se já existe a associação dessa  versao com o cliente e gerar uma página de erro.
    existe = ClientCategoryVersion.objects.filter(clientCat=clientcat, version=version)
    if len(existe) == 1:
        print('já existe a associação dessa versão, renderizar página de erro...')
        return False
        #gerar erro
    else:
        print('não deu erro de associação')
        ClientCategoryVersion.objects.create(clientCat=clientcat, version=version, usuario=usuario)
        return True

def saveBackupRequest(client, version, user):
    checkIfExists = ClientBackup.objects.filter(client=client, solic_version=version)
    if len(checkIfExists) == 1:
        print("Já existe a solicitação de backup par aesta versão, renderizar página de erro...")
        return False
    else:
        print("Não existe ainda a solicitação: Salvar!")
        ClientBackup.objects.create(client=client, solic_version=version, solic_user=user)
        return True

    

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