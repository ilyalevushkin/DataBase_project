# Generated by Django 3.0.6 on 2020-09-04 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virus_app', '0010_auto_20200904_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=20),
        ),
    ]