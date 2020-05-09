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

    is_joinable = models.BooleanField(default=True)

    def __unicode__(self):
        return 'Game #{0}'.format(self.pk)


class GameLog(models.Model):
    game_id = models.TextField()
    text = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Game #{0} Log'.format(self.game.id)


class GameAuthorized(models.Model):
    game_id = models.TextField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __unicode__(self):
        return 'Game #{0} Authorized'.format(self.game_id)


class GameStatistic(models.Model):
    total_accuse = models.IntegerField()
    total_accuse_failed = models.IntegerField()
    total_accuse_success = models.IntegerField()
    total_suggestion = models.IntegerField()

    chosen_professor_plum = models.IntegerField()
    chosen_colonel_mustard = models.IntegerField()
    chosen_mr_green = models.IntegerField()
    chosen_mrs_white = models.IntegerField()
    chosen_ms_scarlet = models.IntegerField()
    chosen_mrs_peacock = models.IntegerField()


