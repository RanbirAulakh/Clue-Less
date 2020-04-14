from django.contrib import admin

from game.models import Game

# register the models to show up in Admin dashboard
admin.site.register(Game)