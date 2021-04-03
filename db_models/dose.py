from django.db import models

class Dose(models.Model):
	LOCATIONS = [("LUA", "Left Upper Arm"),
	("LD", "Left Deltoid"),
	("LGM", "Left Gluteous Medius"),
	("LLF", "Left Lower Forearm"),
	("LT", "Left Thigh"),
	('LVL', "Left Vastus Lateralis"),
	('RUA', "Right Upper Arm"),
	('RD', "Right Deltoid"),
	('RGM', "Right Gluteous Medius"),
	('RLF', "Right Lower Forearm"),
	('RT', "Right Thigh"),
	('RVL', "Right Vastus Lateralis")]

	patient = models.ForeignKey(Patient, on_delete=models.SET_NULL) # should become foreign key
	vaccine = models.ForeignKey(VaccineBatch, on_delete=models.SET_NULL)
	amount = models.FloatField()
	administered = models.CharField(max_length=2)
	location = models.CharField(max_length=3, choices=LOCATIONS)
	vaccinator = models.ForeignKey("Staff", on_delete=models.SET_NULL)
	station = models.ForeignKey("Station", on_delete=models.SET_NULL)
	signIn = models.DateTimeField()
	timeVax = models.DateTimeField()
	slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
	secondDose = models.BooleanField()
