from django.db import models
from models/role import Role
from models/staff import Staff
from models/person import Person
from models/vaccine_type import VaccineType
from models/site import Site
from models/station import Station
from models/vaccine_batch import VaccineBatch
from models/slot import Slot
from models/dose import Dose

# Create your models here.

class Test(models.Model):
	test = models.charField(max_length=10)