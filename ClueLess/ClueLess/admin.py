from django.contrib import admin

from game.models import Game, GameLog, GameAuthorized, GameStatistic
from account.models import UserStatistic

# register the models to show up in Admin dashboard
admin.site.register(Game)
admin.site.register(GameLog)
admin.site.register(GameAuthorized)
admin.site.register(GameStatistic)
admin.site.register(UserStatistic)
