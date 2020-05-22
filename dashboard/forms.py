from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models

class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Digite a senha'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repita a senha'}))
    class Meta:
        model = User
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Usuário'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nome'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Sobrenome'}),
        }
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']