from django.db import models
from ..managers.epidemicmanager import EpidemicManager
from django_countries.fields import CountryField
#official ISO 3166-1 list of countries max_length = 2
#get_FOO_display()
from .epidemiology import Epidemiology


class Epidemic(models.Model):
    source_country_of_infection = CountryField()
    epidemiology = models.ForeignKey(Epidemiology, on_delete = models.PROTECT)

    photo = models.ImageField(
        upload_to='img/epidemic_countries', default='img/epidemic_countries/base_country.jpg'
    )

    more_info = models.TextField(default='Краткие сведения об эпидемии конкретного вируса.')

    objects = EpidemicManager()

    def __str__(self):
        return '{} {}'.format(self.epidemiology.virus.name, self.source_country_of_infection)