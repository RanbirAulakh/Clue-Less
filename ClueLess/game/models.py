from django.db import models

# Create your models here.
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    type = models.CharField(max_length=10)
    # visibility = models.BooleanField()
    private_key = models.TextField()
    # created_by = models.TextField()
    created_date = models.DateField(auto_now_add=True)