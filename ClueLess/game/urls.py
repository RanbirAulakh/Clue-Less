from django.urls import path
from . import views

urlpatterns = [
    path('find_game', views.find_game_page, name='find_game'),
    path('create_game', views.create_game_page, name='create_game'),
    path('game/<int:id>', views.game, name='game'),
]