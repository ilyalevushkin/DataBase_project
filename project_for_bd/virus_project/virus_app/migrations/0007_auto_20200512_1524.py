# Generated by Django 3.0.6 on 2020-05-12 12:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('virus_app', '0006_auto_20200512_1151'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Favorites',
            new_name='Favourites',
        ),
    ]