# Generated by Django 4.1.2 on 2022-12-06 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0016_alter_citizen_friends'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citizen',
            name='friends',
        ),
    ]
