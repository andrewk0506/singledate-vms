from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, ModelChoiceField, ChoiceField, RadioSelect, MultipleChoiceField, CheckboxSelectMultiple, Select
from django.core.validators import validate_email
from phone_field import PhoneField
from .utils import Gender, Race, Ethnicity, AddressType, States, GenerateDBID, CleanCharField
from multiselectfield import MultiSelectField
from .role import Role

class NoCommaField(CleanCharField):
    """
    Helper CharField but with commas replaced by spaces.
    """
    def __init__(self, *args, **kwargs):
        self.max_length = kwargs['max_length']
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        att = getattr(model_instance, self.attname)
        return att.replace(',', ' ')

class Patient(models.Model):
    """
    Table of patient's personal and contact information.
    """

    ### Database Identifier
    dbid = models.CharField(max_length=11, default=GenerateDBID, unique=True)

    ### Personal Data
    person = models.AutoField(primary_key=True)
    first_name = CleanCharField(max_length=100) # Not null by default.
    last_name = CleanCharField(max_length=100)  # Not null by default.
    middle_initial = CleanCharField(max_length=1)
    dob = models.DateField() # Not null by default.
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.F)
    race = MultiSelectField(choices=Race.choices, default=Race.X) # django-multiselectfield calculates the max length automatically
    ethnicity = models.CharField(max_length=1, choices=Ethnicity.choices, default=Ethnicity.X)

    ### Contact Info
    phone = PhoneField(blank=True)
    email = models.EmailField(validators=[validate_email]) # Not null by default.
    street = NoCommaField(max_length=100) # Not null by default.
    city = CleanCharField(max_length=100) # Not null by default.
    zip_code = CleanCharField(max_length=5) # Not null by default.
    state = models.CharField(max_length=2, choices=States.choices, default=States.NJ)
    address_type = models.CharField(max_length=1, choices=AddressType.choices,
                                    default=AddressType.H)

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    last_name = CleanCharField(max_length=100)
    first_name = CleanCharField(max_length=100)
    phone_number = PhoneField(null=True, blank=True)
    email = models.CharField(max_length=60)
    HIPAACert = models.DateTimeField(null=True, blank=True)
    medical_id = models.IntegerField(null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.email

