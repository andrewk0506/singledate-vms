from django.db import models


class Site(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=5, null=True)
    email = models.CharField(max_length=60)
    state = models.CharField(max_length=2, null=True)
    comments = models.TextField(max_length=200)
