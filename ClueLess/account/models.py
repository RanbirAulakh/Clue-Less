from django.db import models

from django.db import models
from django.contrib.auth.models import User


class UserStatistic(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, related_name='user', on_delete=models.DO_NOTHING)
	total_game = models.IntegerField(default=0)
	total_wins = models.IntegerField(default=0)
	total_loss = models.IntegerField(default=0)
	chosen_professor_plum = models.IntegerField(default=0)
	chosen_colonel_mustard = models.IntegerField(default=0)
	chosen_mr_green = models.IntegerField(default=0)
	chosen_mrs_white = models.IntegerField(default=0)
	chosen_ms_scarlet = models.IntegerField(default=0)
	chosen_mrs_peacock = models.IntegerField(default=0)

