from django.db import models
from .site import Site
from .vaccine_type import VaccineType

class VaccineBatch(models.Model):

	class Meta:
		app_label = "vms_app"

	batch = models.IntegerField()
	site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
	vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL, null=True)