from django.db import models
from .site import Site
from .vaccine_type import VaccineType

class Slot(models.Model):

	class Meta:
		app_label = "vms_app"

	site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
	startTime = models.DateTimeField()
	duration = models.SmallIntegerField(3)
	capacity = models.IntegerField()
	vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL, null=True)