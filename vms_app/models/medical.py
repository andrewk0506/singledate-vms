from django.db import models
from .user import Patient
from .scheduling import Site
from .utils import Gender, MedicalQuestionType, CleanCharField

class MedicalEligibilityQuestion(models.Model):
    """
        Medical Eligibility Question schema
    """
    id = models.AutoField(primary_key=True)
    label = CleanCharField(max_length=10)
    language = CleanCharField(max_length=20)
    question = CleanCharField(max_length=255)
    explanation = models.TextField()
    gender = CleanCharField(max_length=1, choices=Gender.choices, default=Gender.F)
    bool = models.BooleanField(default=True)

class MedicalEligibilityAnswer(models.Model):
    """
        Medical Eligibility Answer schema
    """
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    answered = models.DateTimeField()
    answer_bool = models.BooleanField(default=True)
    answer_text = models.TextField()

class MedicalEligibility(models.Model):
    """
        Medical Eligibility Information schema
    """
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    type = CleanCharField(max_length=1, choices=MedicalQuestionType.choices)
    start_date = models.DateField()
    end_date = models.DateField()

