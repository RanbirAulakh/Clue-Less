# Generated by Django 3.0.5 on 2020-04-20 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_auto_20200416_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='required_players',
            field=models.CharField(default=4, max_length=2),
            preserve_default=False,
        ),
    ]
