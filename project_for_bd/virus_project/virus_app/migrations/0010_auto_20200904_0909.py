# Generated by Django 3.0.6 on 2020-09-04 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virus_app', '0009_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.TextField(blank=True),
        ),
    ]