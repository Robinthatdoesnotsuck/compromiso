from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    type_of = forms.CharField()
    class Meta:
        model = User
        fields = ["username", "email", "type_of", "password1","password1"]