from django.urls import path
from . import views

urlpatterns = [
    path('find_game', views.find_game_page, name='find_game'),
    path('create_game', views.create_game_page, name='create_game'),
    path('game/<int:game_id>', views.game, name='game'),
    path('enter_pass/<int:game_id>', views.enter_pass, name='enter_pass'),
    path('recent_game/<int:game_id>', views.recent_game, name='recent_game'),
]
