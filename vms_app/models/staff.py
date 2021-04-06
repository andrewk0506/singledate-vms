from django.db import models
from .role import Role

class Staff(models.Model):
	
	class Meta:
		app_label = "vms_app"

	surName = models.CharField(max_length=100)
	givenName = models.CharField(max_length=100)
	phoneNumber = models.CharField(max_length=40)
	email = models.CharField(max_length=60)
	medicalId = models.DecimalField(decimal_places=0, max_digits=10)
	HIPAACert = models.DateTimeField()
	password = models.CharField(max_length=60)
	role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
