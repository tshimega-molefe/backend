# Generated by Django 4.1.2 on 2022-12-06 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0018_citizen_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='friends_list', to='user.citizen'),
        ),
    ]