# Generated by Django 3.0.5 on 2020-05-09 23:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.TextField()),
                ('text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_accuse', models.IntegerField()),
                ('total_accuse_failed', models.IntegerField()),
                ('total_accuse_success', models.IntegerField()),
                ('total_suggestion', models.IntegerField()),
                ('chosen_professor_plum', models.IntegerField()),
                ('chosen_colonel_mustard', models.IntegerField()),
                ('chosen_mr_green', models.IntegerField()),
                ('chosen_mrs_white', models.IntegerField()),
                ('chosen_ms_scarlet', models.IntegerField()),
                ('chosen_mrs_peacock', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GameAuthorized',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField()),
                ('type', models.CharField(max_length=10)),
                ('required_players', models.CharField(max_length=2)),
                ('private_key', models.TextField(blank=True, null=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('completed_date', models.DateTimeField(blank=True, null=True)),
                ('is_joinable', models.BooleanField(default=True)),
                ('winner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='winner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
