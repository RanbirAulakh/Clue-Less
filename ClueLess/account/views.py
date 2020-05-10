from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from . import forms
from . import models


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)

            # create personal stats
            user_stats = models.UserStatistic(user=request.user)
            user_stats.save()
            return redirect('/')
    else:
        form = forms.RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """
    Cannot use def login since django has a built-in login method
    """
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'form': form, 'error': True})
    else:
        form = forms.LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')

