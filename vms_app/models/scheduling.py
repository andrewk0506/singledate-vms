from django.db import models
from .utils import States

class Site(models.Model):
    class Meta:
        app_label = "vms_app"

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=5)
    state = models.CharField(max_length=2, choices=States.choices(), default=States.NJ)
    comments = models.TextField()

    def __str__(self):
        stringFormat = "{street}, {city}, {state}, {zipCode}".format(
            street=self.street,
            city=self.city,
            state=self.state,
            zipCode=self.zipCode,
        )
        return stringFormat


class Station(models.Model):
    class Meta:
        app_label = "vms_app"

    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    stationName = models.CharField(max_length=50, default=None, null=True)

class Slot(models.Model):

	class Meta:
		app_label = "vms_app"

	site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
	startTime = models.DateTimeField()
	duration = models.SmallIntegerField(3)
	capacity = models.IntegerField()

    # to avoid circular import  used string
	vaccineType = models.ForeignKey(
        'vms_app.VaccineType',
        on_delete=models.SET_NULL,
        null=True
        )

