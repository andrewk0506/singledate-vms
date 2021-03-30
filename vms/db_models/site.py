from django.db import models

class Site(models.Model):
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	zipcode = models.CharField(max_length=5)
	state = models.CharField(max_length=2)
	comments = models.TextField()