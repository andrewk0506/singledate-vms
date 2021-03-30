from django.db import models

class VaccineBatch(models.Model):
	batch = models.IntegerField()
	site = models.ForeignKey(Site, on_delete=models.SET_NULL)
	vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL)