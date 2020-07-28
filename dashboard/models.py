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

# Criar um model para versão
# Criar um padrão igual ao de cadastro do cliente na opção de atualizar
# Trazer o usuário logado
# Puxar data e hora do momento