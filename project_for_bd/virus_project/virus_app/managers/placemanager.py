from django.db import models


class PlaceManager(models.Manager):
    def get_all_places_for_cur_epidemic(self, epidemic_pk):
        return self.filter(placedemography__epidemic=epidemic_pk)