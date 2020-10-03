# Generated by Django 3.0.6 on 2020-05-11 08:11

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Epidemic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_country_of_infection', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Epidemiology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('structure', models.CharField(choices=[('Кп', 'Капсид'), ('С', 'Спиральный'), ('И', 'Икосаэдрический'), ('П', 'Продолговатый'), ('Км', 'Комплексный'), ('О', 'Оболочка')], max_length=2)),
                ('source_of_infection', models.CharField(choices=[('Ант', 'Антропоноз'), ('Зоо', 'Зооноз'), ('За', 'Зооантропоноз')], max_length=3)),
                ('transmission_mechanism', models.CharField(choices=[('Аэ', 'Аэрогенный'), ('Кн', 'Контактный'), ('Тр', 'Трансмиссивный'), ('Фо', 'Фекально-оральный'), ('Вр', 'Вертикальный'), ('Гм', 'Гемоконтактный')], max_length=2)),
                ('symptoms', models.TextField()),
                ('more_info', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Period',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(default=datetime.date(1300, 1, 1))),
                ('date_to', models.DateField(default=datetime.date(1300, 1, 1))),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('town', models.CharField(max_length=100, unique=True)),
                ('region', models.CharField(choices=[('СА', 'Северная Америка'), ('ЮА', 'Южная Америка'), ('Аф', 'Африка'), ('Е', 'Европа'), ('Аз', 'Азия'), ('Ав', 'Австралия'), ('Ан', 'Антарктида')], max_length=2)),
                ('population', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='PlaceOfBeating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_of_beating', models.CharField(choices=[('Одс', 'Опорно-двигательная система'), ('Пщс', 'Пищеварительная система'), ('Дс', 'Дыхательная система'), ('Мс', 'Мочевыделительная система'), ('Рс', 'Репродуктивные органы'), ('Эж', 'Эндокринные железы'), ('Ск', 'Система кровообращения'), ('Нс', 'Нервная система'), ('Пкс', 'Покровная система')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='TransmissionWays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transmission_way', models.CharField(choices=[('Ал', 'Алиментарный'), ('Вод', 'Водный'), ('Кб', 'Контактно-бытовой'), ('Ук', 'Укус'), ('Пар', 'Парентеральный'), ('По', 'Половой'), ('Вк', 'Воздушно-капельный'), ('Вп', 'Воздушно-пылевой'), ('Ран', 'Раневой'), ('Кп', 'Контактно-половой')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Virus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, unique=True)),
                ('photo', models.ImageField(default='static/img/viruses/base_virus.jpg', upload_to='static/img/viruses')),
                ('epidemiology', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='virus_app.Epidemiology')),
            ],
        ),
        migrations.CreateModel(
            name='PlaceDemography',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infected', models.PositiveIntegerField(default=0)),
                ('recovered', models.PositiveIntegerField(default=0)),
                ('dead', models.PositiveIntegerField(default=0)),
                ('epidemic', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemic')),
                ('period', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='virus_app.Period')),
                ('place', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='virus_app.Place')),
            ],
        ),
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('more_info', models.TextField()),
                ('epidemic', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemic')),
                ('place_demography', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.PROTECT, to='virus_app.PlaceDemography')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('virus', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='virus_app.Virus')),
            ],
        ),
        migrations.AddField(
            model_name='epidemiology',
            name='place_of_beating',
            field=models.ManyToManyField(to='virus_app.PlaceOfBeating'),
        ),
        migrations.AddField(
            model_name='epidemiology',
            name='transmission_way',
            field=models.ManyToManyField(blank=True, to='virus_app.TransmissionWays'),
        ),
        migrations.AddField(
            model_name='epidemic',
            name='epidemiology',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='virus_app.Epidemiology'),
        ),
    ]