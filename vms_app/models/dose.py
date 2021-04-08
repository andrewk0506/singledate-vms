from django.db import models
from .vaccine_batch import VaccineBatch
from .slot import Slot
from .user import Patient, Staff
from .station import Station


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
    )  # should become foreign key
    vaccine = models.ForeignKey(VaccineBatch, on_delete=models.SET_NULL, null=True)
    administered = models.CharField(max_length=2, null=True)
    location = models.CharField(max_length=3, choices=LOCATIONS, null=True)
    vaccinator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    signIn = models.DateTimeField(null=True)
    timeVax = models.DateTimeField(null=True)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    secondDose = models.BooleanField()
