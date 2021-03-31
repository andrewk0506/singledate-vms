from django.db import models

class VaccineType(models.Model):
	name = models.CharField(max_length=100)
	daysUntilNext = models.IntegerField()
