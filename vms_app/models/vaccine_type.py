from django.db import models


class VaccineType(models.Model):
    class Meta:
        app_label = "vms_app"

    name = models.CharField(max_length=100)
    daysUntilNext = models.IntegerField()
    amount = models.FloatField()
