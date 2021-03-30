from django.db import models

class Slot(models.Model):
	site = models.ForeignKey(Site, on_delete=models.SET_NULL)
	startTime = models.DateTimeField()
	duration = models.SmallIntegerField(3)
	capacity = models.IntegerField()
	vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL)