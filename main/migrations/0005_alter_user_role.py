# Generated by Django 5.1 on 2024-08-24 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_remove_events_event_organiser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('organizer', 'Organizer'), ('user', 'User')], default='user', max_length=10),
        ),
    ]
