from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from game import models as Game
from account import models as Account

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
    global_statistics = Game.GameStatistic.objects.get(id=1)

    characters = {
        "Professor Plum": global_statistics.chosen_professor_plum,
        "Colonel Mustard": global_statistics.chosen_colonel_mustard,
        "Mr Green": global_statistics.chosen_mr_green,
        "Mrs White": global_statistics.chosen_mrs_white,
        "Ms Scarlet": global_statistics.chosen_ms_scarlet,
        "Mrs Peacock": global_statistics.chosen_mrs_peacock,
    }

    most_chosen_character = max(characters, key=characters.get)

    user_statistic = ""
    user_most_chosen_character = ""
    if request.user.is_authenticated:
        user_statistic = Account.UserStatistic.objects.get(user=request.user)
        user_characters = {
            "Professor Plum": user_statistic.chosen_professor_plum,
            "Colonel Mustard": user_statistic.chosen_colonel_mustard,
            "Mr Green": user_statistic.chosen_mr_green,
            "Mrs White": user_statistic.chosen_mrs_white,
            "Ms Scarlet": user_statistic.chosen_ms_scarlet,
            "Mrs Peacock": user_statistic.chosen_mrs_peacock,
        }
        user_most_chosen_character = max(user_characters, key=user_characters.get)

    return render(request, 'statistic.html', {'users_count': users_count,
                                              'total_games': total_games,
                                              'global_statistics': global_statistics,
                                              "most_chosen_character": most_chosen_character,
                                              "user_stats": user_statistic,
                                              "user_most_chosen_character": user_most_chosen_character})
