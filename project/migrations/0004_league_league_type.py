# Generated by Django 4.2.16 on 2024-11-21 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_remove_league_league_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='league_type',
            field=models.CharField(blank=True, choices=[('Premier League', 'Premier League'), ('La Liga', 'La Liga'), ('Serie A', 'Serie A')], max_length=50, null=True),
        ),
    ]
