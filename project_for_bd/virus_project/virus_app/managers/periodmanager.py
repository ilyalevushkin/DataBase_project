from django.db import models


class PeriodManager(models.Manager):
    def get_all_periods_for_cur_epidemic(self, epidemic_pk):
        return self.filter(placedemography__epidemic=epidemic_pk).order_by('date_from')