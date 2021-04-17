from django.db import models
from django.forms import ModelForm, ModelChoiceField, ChoiceField, RadioSelect, MultipleChoiceField, CheckboxSelectMultiple, Select
from django.core.validators import validate_email
from phone_field import PhoneField
from .utils import Gender, Race, Ethnicity, AddressType, States
from multiselectfield import MultiSelectField

class NoCommaField(models.CharField):
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
    ### Personal Data
    person = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100) # Not null by default.
    last_name = models.CharField(max_length=100)  # Not null by default.
    middle_initial = models.CharField(max_length=1)
    dob = models.DateField() # Not null by default.
    gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.F)
    race = MultiSelectField(choices=Race.choices, default=Race.X) # django-multiselectfield calculates the max length automatically 
    ethnicity = models.CharField(max_length=1, choices=Ethnicity.choices, default=Ethnicity.X)
    
    ### Contact Info
    phone = PhoneField(blank=True)
    email = models.EmailField(validators=[validate_email]) # Not null by default.
    street = NoCommaField(max_length=100) # Not null by default.
    city = models.CharField(max_length=100) # Not null by default.
    zip_code = models.CharField(max_length=5) # Not null by default.
    state = models.CharField(max_length=2, choices=States.choices, default=States.NJ)
    address_type = models.CharField(max_length=1, choices=AddressType.choices,
                                    default=AddressType.H)

class Staff(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60, null=True)
    HIPAACert = models.DateTimeField(null=True, blank=True)
    medical_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=60)


# class PatientForm(ModelForm):
#     class Meta:
#         model = Patient
#         # exclude = ['race']
#         fields = ['first_name',
#                   'last_name',
#                   'gender',
#                   'dob',
#                   'ethnicity',
#                   'email',
#                   'phone',
#                   'address_type',
#                   'street',
#                   'zip_code',
#                   'city',
#                   'state']

#     # TODO: Add race as a question
#     #       Probably involves changing the model type

#     gender = ChoiceField(choices=Gender.choices, widget=RadioSelect())
#     # race = MultipleChoiceField(choices=Race.choices, widget=CheckboxSelectMultiple())
#     ethnicity = ChoiceField(choices=Ethnicity.choices, widget=RadioSelect())
#     # state = ChoiceField(choices=States.choices, widget=Select())
#     address_type = ChoiceField(choices=AddressType.choices, widget=RadioSelect())