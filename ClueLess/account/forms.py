from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    win = 0
    loss = 0
    games_played = 0

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
