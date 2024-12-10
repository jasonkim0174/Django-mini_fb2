# Generated by Django 4.2.16 on 2024-11-20 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='stadium',
        ),
        migrations.AddField(
            model_name='league',
            name='league_type',
            field=models.CharField(choices=[('domestic', 'Domestic'), ('international', 'International'), ('friendly', 'Friendly')], default='domestic', max_length=20),
        ),
    ]
