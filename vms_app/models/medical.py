from django.db import models
# from .user import Patient
from .utils import Gender


class MedicalEligibilityQuestion(models.Model):
    """
        Medical Eligibility Question schema
    """

    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=10)
    language = models.CharField(max_length=20)
    question = models.CharField(max_length=255)
    explanation = models.TextField()
    gender = models.CharField(max_length=1, choices=Gender.choices(), default=Gender.F)
    bool = models.BooleanField(default=True)

class MedicalEligibilityAnswer(models.Model):
    """
        Medical Eligibility Answer
    """
    # person = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    answered = models.DateTimeField()
    answer_bool = models.BooleanField(default=True)
    answer_text = models.TextField()


class MedicalEligibility(models.Model):
    """
    
    """
    QUESTION_TYPE = [('S', 'Screening'), ('E', 'Eligibility')]
    
    # site = models.ForeignKey(Site)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=QUESTION_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()