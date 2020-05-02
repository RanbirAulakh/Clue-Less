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

                if m.type == "Private":
                    game_auth_model = models.GameAuthorized(game_id=m.id, user_id=request.user.id)
                    game_auth_model.save()

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

    if game_details.is_joinable:
        if game_details.type == 'Private':
            if auth_game_user(game_id, request.user.id):
                return render(request, 'game.html', {'game_details': game_details})
            else:
                return redirect('/enter_pass/{0}'.format(game_id))
        else:
            return render(request, 'game.html', {'game_details': game_details})
    else:
        return redirect('find_game')


def auth_game_user(game_id, user_id):
    game_authorized = models.GameAuthorized.objects.filter(game_id=game_id)
    for i in game_authorized:
        if i.user_id == user_id:
            return True

    return False


def enter_pass(request, game_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    game_details = models.Game.objects.get(id=game_id)

    if auth_game_user(game_id, request.user.id):
        return redirect('/game/{0}'.format(game_id))

    if request.method == 'POST':
        form = forms.GameAuthPass(request.POST)
        if form.is_valid():
            fields = form.cleaned_data
            private_key = fields.get('private_key')

            if private_key == game_details.private_key:
                g = models.GameAuthorized(game_id=game_id, user_id=request.user.id)
                g.save()

                return redirect('/game/{0}'.format(game_id))
            else:
                return render(request, 'enter_pass.html', {'id': game_details.id, 'form': form,
                                                           'error': True, 'error_msg': "Incorrect Game Password!"})

    else:
        form = forms.GameAuthPass()

    return render(request, 'enter_pass.html', {'id': game_details.id, 'form': form})
