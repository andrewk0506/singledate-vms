from django.db import models
from .role import Role

class Staff(models.Model):
	
	class Meta:
		app_label = "vms_app"

	surName = models.charField(max_length=100)
	givenName = models.charField(max_length=100)
	phoneNumber = models.charField(max_length=40)
	email = models.charField(max_length=60)
	medicalId = models.decimalField(max_digits=10)
	HIPAACert = models.DateTimeField()
	password = models.charField(max_length=60)
	role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
