from django.db import models
from .staff import Staff


class Log(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    ipAddress = models.CharField(max_length=40)
    webRequest = models.CharField(max_length=64)
    tableName = models.CharField(max_length=100)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    alteredObject = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.ipAddress}"
