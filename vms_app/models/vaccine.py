from django.db import models
from .scheduling import Site, Station, Slot
from .user import Patient, Staff

class VaccineType(models.Model):
    class Meta:
        app_label = "vms_app"

    name = models.CharField(max_length=100)
    daysUntilNext = models.IntegerField()
    amount = models.FloatField()


class VaccineBatch(models.Model):
    class Meta:
        app_label = "vms_app"

    batch = models.IntegerField()
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL, null=True)
    expiration = models.DateTimeField(null=True)

class Dose(models.Model):
    class Meta:
        app_label = "vms_app"

    LOCATIONS = [
        ("LUA", "Left Upper Arm"),
        ("LD", "Left Deltoid"),
        ("LGM", "Left Gluteous Medius"),
        ("LLF", "Left Lower Forearm"),
        ("LT", "Left Thigh"),
        ("LVL", "Left Vastus Lateralis"),
        ("RUA", "Right Upper Arm"),
        ("RD", "Right Deltoid"),
        ("RGM", "Right Gluteous Medius"),
        ("RLF", "Right Lower Forearm"),
        ("RT", "Right Thigh"),
        ("RVL", "Right Vastus Lateralis"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.SET_NULL, null=True
    ) 
    vaccine = models.ForeignKey(VaccineBatch, on_delete=models.SET_NULL, null=True)
    administered = models.CharField(max_length=2, null=True)
    location = models.CharField(max_length=3, choices=LOCATIONS, null=True)
    vaccinator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    signIn = models.DateTimeField(null=True)
    timeVax = models.DateTimeField(null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    secondDose = models.BooleanField()
    notes = models.TextField(default="")
