from django.db import models
from .site import Site


class Station(models.Model):
    class Meta:
        app_label = "vms_app"

    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    stationName = models.CharField(max_length=50, default=None, null=True)
