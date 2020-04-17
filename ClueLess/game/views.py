from django.shortcuts import render, redirect
from . import forms
from . import models

# Create your views here.


def find_game_page(request):
    if request.user.is_authenticated:
        games = models.Game.objects.all()
        return render(request, 'find_game.html', {'list_games': games})
    else:
        return redirect('/login')


def create_game_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.GameForm(request.POST)
            if form.is_valid():
                m = form.save()
                return redirect('/game/{0}'.format(m.id))
        else:
            form = forms.GameForm()
    else:
        return redirect('/login')

    return render(request, 'create_game.html', {'form': form})


def game(request, game_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    game_details = models.Game.objects.get(id=game_id)
    return render(request, 'game.html', {'game_details': game_details})
