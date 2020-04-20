from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField(null=False)
    type = models.CharField(max_length=10)
    required_players = models.CharField(max_length=2)
    private_key = models.TextField(null=True, blank=True)

    created_date = models.DateField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)  # if game is completed
    winner = models.ForeignKey(User, null=True, blank=True, related_name='winner', on_delete=models.DO_NOTHING)

    current_turn = models.ForeignKey(User, null=True, blank=True, related_name='current_turn', on_delete=models.DO_NOTHING)
    is_joinable = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)


class GameLog(models.Model):
    game = models.ForeignKey(Game, on_delete=models.DO_NOTHING)
    text = models.TextField()

    created_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return 'Game #{0} Log'.format(self.game.id)