from django.db import models
from .transmissionways import TransmissionWays
from .placeofbeating import PlaceOfBeating
from ..managers.epidemiologymanager import EpidemiologyManager

class Epidemiology(models.Model):
    structure_choices = (
        ('С' , 'Спиральный'),
        ('И' , 'Икосаэдрический'),
        ('П' , 'Продолговатый'),
        ('Км' , 'Комплексный'),
    )
    structure = models.CharField(max_length=2, choices=structure_choices)
    source_choices = (
        ('Ант' , 'Антропоноз'),
        ('Зоо' , 'Зооноз'),
        ('За' , 'Зооантропоноз'),
    )
    source_of_infection = models.CharField(max_length = 3, choices = source_choices)
    transmission_choices = (
        ('Аэ' , 'Аэрогенный'),
        ('Кн' , 'Контактный'),
        ('Тр' , 'Трансмиссивный'),
        ('Фо' , 'Фекально-оральный'),
        ('Вр' , 'Вертикальный'),
        ('Гм' , 'Гемоконтактный'),
    )
    transmission_mechanism = models.CharField(max_length=2, choices=transmission_choices)

    transmission_way = models.ManyToManyField(TransmissionWays, blank=True)

    place_of_beating = models.ManyToManyField(PlaceOfBeating, blank = False)

    symptoms = models.TextField()

    more_info = models.TextField()

    objects = EpidemiologyManager()

    def __str__(self):
        return '{} {}'.format(self.get_source_of_infection_display(), self.get_transmission_mechanism_display())