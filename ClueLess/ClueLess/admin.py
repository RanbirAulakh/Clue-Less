from django.contrib import admin

from game.models import Game, GameLog

# register the models to show up in Admin dashboard
admin.site.register(Game)
admin.site.register(GameLog)