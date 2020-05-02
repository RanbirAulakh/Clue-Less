from django.contrib import admin

from game.models import Game, GameLog, GameAuthorized

# register the models to show up in Admin dashboard
admin.site.register(Game)
admin.site.register(GameLog)
admin.site.register(GameAuthorized)
