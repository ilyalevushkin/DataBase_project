from django.db import models
from ..managers.placedemographymanager import PlaceDemographyManager
from .epidemic import Epidemic
from .period import Period
from .place import Place





class PlaceDemography(models.Model):
    infected = models.PositiveIntegerField(default=0)
    recovered = models.PositiveIntegerField(default=0)
    dead = models.PositiveIntegerField(default=0)
    epidemic = models.ForeignKey(Epidemic, on_delete = models.PROTECT)
    period = models.ForeignKey(Period, on_delete = models.PROTECT)
    place = models.ForeignKey(Place, on_delete= models.PROTECT)

    objects = PlaceDemographyManager()

    def __str__(self):
        return '{} {} {}'.format(self.infected, self.recovered, self.dead)