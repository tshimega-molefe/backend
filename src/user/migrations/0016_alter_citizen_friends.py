# Generated by Django 4.1.2 on 2022-12-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_citizen_friends'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='friends',
            field=models.ManyToManyField(blank=True, to='user.citizen'),
        ),
    ]