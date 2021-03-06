# Generated by Django 3.0.6 on 2020-09-14 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('virus_app', '0015_auto_20200914_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='epidemic',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemic'),
        ),
        migrations.AlterField(
            model_name='country',
            name='favourite',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Favourites'),
        ),
        migrations.AlterField(
            model_name='region',
            name='epidemic',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemic'),
        ),
        migrations.AlterField(
            model_name='region',
            name='favourite',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Favourites'),
        ),
        migrations.AlterField(
            model_name='town',
            name='epidemic',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemic'),
        ),
        migrations.AlterField(
            model_name='town',
            name='favourite',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Favourites'),
        ),
    ]
