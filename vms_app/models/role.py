from django.db import models

class Role(models.Model):

	class Meta:
		app_label = "vms_app"

	role = models.charField(max_length=15)