from django.db import models
from .forms import CreateUserForm
from django.contrib.auth.models import User
import uuid
#import re

class Cliente(models.Model):
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=12, null=False)
    email = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    div_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(upload_to='static/profiles/', blank=True)

    def __str__(self):
        return '[' +str(self.id) +'] ' + self.user.first_name + ' ' + self.user.last_name

class ClientCategory(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False, unique=True)
    icon = models.CharField(max_length=100)
    
    def __str__(self):
        return '[' + str(self.id) +'] ' + self.name

class ClientCategoryRelation(models.Model):
    categorie = models.ForeignKey(ClientCategory, null=True, on_delete=models.SET_NULL)
    client = models.ForeignKey(Cliente, null=True, on_delete=models.SET_NULL)
    url = models.CharField(max_length=150, null=True, blank=True)
    urlcentral = models.CharField(max_length=150, null=True, blank=True)

    class Meta:
        unique_together =('categorie', 'client')

    def __str__(self):
        return ('[' 
        + str(self.id) 
        + '] ' 
        + self.client.name 
        + ' (' 
        + self.categorie.name
        + ')')

class CategoryVersion(models.Model):
    category = models.ForeignKey(ClientCategory, null=False, on_delete=models.CASCADE)
    version = models.CharField(max_length=10)
    def __str__(self):
        return('['
        +str(self.id)
        +'] '
        +self.category.name
        +' - '
        +self.version
        )

class ClientCategoryVersion(models.Model):
    clientCat = models.ForeignKey(ClientCategoryRelation, null=False, on_delete=models.CASCADE)
    #version = models.CharField(max_length=10)
    version = models.ForeignKey(CategoryVersion, on_delete=models.CASCADE, null=False)
    dataHora = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return(
        self.clientCat.client.name +' - '
        +self.clientCat.categorie.name +' ( '
        +self.version.version +' ) '
        +str(self.dataHora)
        )

class BackupDestination(models.Model):
    name = models.CharField(max_length=80, null=False)
    user = models.CharField(max_length=80, null=False)
    password = models.CharField(max_length=80, null=False)
    address = models.CharField(max_length=150, null=False)
    obs = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return(
        self.name
        +' - '
        +self.user
        )

class ClientBackup(models.Model):
    STATUS = (
        ('P', 'Pendente'),
        ('C', 'Cancelado'),
        ('F', 'Finalizado'),
    )
    client = models.ForeignKey(ClientCategoryRelation, null=False, on_delete=models.CASCADE)
    solic_date = models.DateTimeField(auto_now_add=True)    
    solic_version = models.ForeignKey(ClientCategoryVersion, null=False, on_delete=models.CASCADE)
    solic_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='solicitante')
    atend_date = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    atend_user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='atendente')
    status = models.CharField(max_length=1, choices=STATUS)
    destination = models.ForeignKey(BackupDestination, null=True, blank=True, on_delete=models.SET_NULL)
    localizacao = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return(
            self.solic_version.version.version            
            + ' - '
            + str(self.solic_date)
            + ' - '
            + self.get_status_display()
        )



'''
-->
Desenhar a tela de solicitação
Fazer funcionar o botão solicitar
Criar uma variável, para descobrir de onde veio antes de solicitar.
Resolver a dashboard, mostrar cliente com categoria
Gravar solicitaçãO
Devolver o usuário pro mesmo lugar
Não permitir solicitar se já houver uma solicitação pendente


Na questao de atendimento:
É preciso construir uma lista para cadastros dos FTP's que será utilizada no atendimento
Durante o atendimento foram decididos os formatos de entrega abaixo:

C:\Minha pasta\Qualquer coisa

\\192.169.0.137\Bancos de Dados\Eliu\

ftp.assessorpublico.com.br publicoftp:9kam8rez \eliu\birigui\

Deverá ser construído um padrão para o terceiro.
FTP, nome do FTP, usuário e senha serão cadastrados.

O Status irá mudar para finalizado

Trazer os campos:
Usuário de atendimento: Preenchido
Destino: Lista para seleção
Localização: Campo para preenchimento
Status: Mudar automaticamente para finalizado
Data: Buscar automaticamente

Dar a opção para o atendente selecionar
Trazer o valor como chave estrangeira
Caso opte por não selecionar
Apenas preencher o valor do caminho que será salvo no campo localizacao.

Fazer funcionar o botão atender
Desenhar a tela de atendimento

Finalizar tela de locais: Salvar, apresentar lista ao salvar,


criar uma página de edição, criar função de inativação;

Criar função de inverter barra

Ao criar local definir tipo:
Web
FTP
Rede Interna

Inverter barra ao exibir na página do cliente.


Verificar se o cliente tem solicitação pendente
Caso sim exibir o botão atender
Caso não, deixar inativo...

Refazer a ordem do local onde o backup está salvo: \\192.168.0.137\Bancos de dados\eliu\
colocar a opção de copiar e colar na página dashboard

-----

INICIAR A FUNÇÃO DE CRIAÇÃO DO MODELO DE SERVIÇOS

Criar opção de contatos na página do cliente:
Backup, Serviços, Atualizações, Contatos

Ou jogar contatos como parte do serviços...
Analisar melhor...


Acertar cores dos menus

------

COLOCAR DADOS DE CADASTRO DO CLIENTE NA CATEGORIA

MELHORAR TELA DE CADASTRO DE CATEGORIA, 
POSSIBILITANDO CRIAR DURANTE O CADASTRO DO CLIENTE


'''