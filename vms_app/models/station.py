from django.db import models
from .site import Site


class Station(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    station_name = models.CharField(max_length=100)
