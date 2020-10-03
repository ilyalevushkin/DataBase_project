from django.db import models
from ..managers.placemanager import PlaceManager
from django_countries.fields import CountryField


class Place(models.Model):
    country = CountryField()
    town = models.CharField(max_length=100)

    region_choices = (
        ('СА', 'Северная Америка'),
        ('ЮА', 'Южная Америка'),
        ('Аф', 'Африка'),
        ('Е', 'Европа'),
        ('Аз', 'Азия'),
        ('Ав', 'Австралия'),
        ('Ан', 'Антарктида'),
    )

    region = models.CharField(max_length=2, choices=region_choices)
    population = models.PositiveIntegerField(default=0)

    objects = PlaceManager()

    def __str__(self):
        return '{} {}'.format(self.country, self.population)