from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from game import models as Game

# Create your views here.
def index(request):
    users_count = len(User.objects.all())
    total_games = len(Game.Game.objects.all())
    return render(request, 'index.html', {'users_count': users_count, 'total_games': total_games})


def help_page(request):
    return render(request, 'help.html')


def about_page(request):
    return render(request, 'about.html')


def statistic_page(request):
    users_count = len(User.objects.all())
    total_games = len(Game.Game.objects.all())
    return render(request, 'statistic.html', {'users_count': users_count, 'total_games': total_games})