from django.db import models

from ..managers.virusmanager import VirusManager
from .epidemiology import Epidemiology


class Virus(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)
    epidemiology = models.OneToOneField(Epidemiology, on_delete = models.CASCADE)
    photo = models.ImageField(
        upload_to='img/viruses', default='img/viruses/base_virus.jpg'
    )

    objects = VirusManager()

    def __str__(self):
        return self.name