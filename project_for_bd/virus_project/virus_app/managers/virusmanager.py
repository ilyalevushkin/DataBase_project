from django.db import models


class VirusManager(models.Manager):
    def base_information(self):
        return self.order_by('name')

    def current_virus(self, pk):
        return self.get(pk=pk)

