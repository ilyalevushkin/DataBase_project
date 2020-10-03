from django.db import models
from ..managers.periodmanager import PeriodManager
import datetime



class Period(models.Model):
    default_date = datetime.date(1300, 1, 1)
    date_from = models.DateField(default = default_date)
    date_to = models.DateField(default = default_date)
    if (date_from >= date_to):
        raise Exception('Дата до больше чем дата после')

    objects = PeriodManager()

    def __str__(self):
        return '{} {}'.format(self.date_from, self.date_to)