# Generated by Django 4.2.16 on 2024-11-21 03:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_remove_team_stadium_league_league_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='league',
            name='league_type',
        ),
    ]
