from django.shortcuts import render, redirect
from . import forms
from . import models

# Create your views here.


def find_game_page(request):
    if request.user.is_authenticated:
        games = models.Create.objects.all()
        return render(request, 'find_game.html', {'list_games': games})
    else:
        return redirect('/login')


def create_game_page(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = forms.CreateGameForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'game.html')
        else:
            form = forms.CreateGameForm()
    else:
        return redirect('/login')

    return render(request, 'create_game.html', {'form': form})


def game(request, id):
    game_details = models.Create.objects.get(id=id)
    print(game_details.type)
    return render(request, 'game.html', {'game_details': game_details})
