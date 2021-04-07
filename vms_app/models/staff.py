from django.db import models


class Staff(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60, null=True)
    HIPAACert = models.DateTimeField(null=True, blank=True)
    medical_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=60)
