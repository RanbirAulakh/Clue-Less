from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from . import forms
from . import models


def find_game_page(request):
    if request.user.is_authenticated:
        games = models.Game.objects.all()

        joinable_games = []
        finished_games = []

        for i in games:
            if not i.winner:
                is_joinable = i.is_joinable
                if not i.is_joinable:
                    is_joinable = auth_game_user(i.id, request.user.id)

                joinable_games.append({"id": i.id, "name": i.name, "created_date": i.created_date, "type": i.type,
                                       "is_joinable": is_joinable})
            else:
                finished_games.append({"id": i.id, "name": i.name, "created_date": i.created_date, "type": i.type,
                                       "winner": i.winner})

        return render(request, 'find_game.html', {'list_games': joinable_games, 'finished_games': finished_games})
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

                # create game log
                game_log_model = models.GameLog(game_id=m.id)
                game_log_model.save()

                return redirect('/game/{0}'.format(m.id))
        else:
            form = forms.GameForm()
    else:
        return redirect('/login')

    return render(request, 'create_game.html', {'form': form})


def game(request, game_id):
    if not request.user.is_authenticated:
        return redirect('/login')

    try:
        game_details = models.Game.objects.get(id=game_id)
    except:
        return render(request, "404.html")

    if not game_details.is_joinable and game_details.type == 'Public':  # if game is not joinable but user accidently refresh the page
        if auth_game_user(game_id, request.user.id):
            return render(request, 'game.html', {'game_details': game_details})
    elif not game_details.is_joinable and game_details.type == 'Private':   # if game is not joinable but user accidently refresh the page
        if auth_game_user(game_id, request.user.id):
            return render(request, 'game.html', {'game_details': game_details})
    else:
        if game_details.is_joinable:
            if game_details.type == 'Private':
                if auth_game_user(game_id, request.user.id):
                    return render(request, 'game.html', {'game_details': game_details})
                else:
                    return redirect('/enter_pass/{0}'.format(game_id))
            else:  # if public game
                if not auth_game_user(game_id, request.user.id):
                    g = models.GameAuthorized(game_id=game_id, user_id=request.user.id)
                    g.save()

                return render(request, 'game.html', {'game_details': game_details})

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


def recent_game(request, game_id):
    try:
        game_details = models.Game.objects.get(id=game_id)
    except:
        return render(request, "404.html")

    if not game_details.winner:
        return redirect('find_game')
    else:
        game_log = models.GameLog.objects.get(game_id=game_id)

        return render(request, 'recent_game.html', {'game_details': game_details, "game_log": game_log})
