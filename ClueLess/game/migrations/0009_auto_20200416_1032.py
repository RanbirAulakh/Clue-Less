# Generated by Django 3.0.5 on 2020-04-16 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20200415_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='private_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
