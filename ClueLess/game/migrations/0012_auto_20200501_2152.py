# Generated by Django 3.0.5 on 2020-05-01 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_gameauthorized'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gameauthorized',
            name='game',
        ),
        migrations.AddField(
            model_name='gameauthorized',
            name='game_id',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
