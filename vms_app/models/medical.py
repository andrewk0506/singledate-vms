from django.db import models
from .utils import Gender

class MedicalElgibility(models.Model):
    """
        Medical Eligibility schema
    """

    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=10)
    language = models.CharField(max_length=20)
    question = models.CharField(max_length=255)
    explanation = models.TextField()
    gender = models.CharField(max_length=1, choices=Gender.choices(), default=Gender.F)
    bool = models.BooleanField(default=True)

