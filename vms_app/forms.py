from django.forms import ModelForm, ModelChoiceField, ChoiceField, RadioSelect, MultipleChoiceField, CheckboxSelectMultiple, Select
from .models import MedicalEligibilityAnswer, Patient
from .models.utils import Gender, Ethnicity, AddressType


class MedicalEligibilityAnswerForm(ModelForm):
    class Meta:
        model = MedicalEligibilityAnswer
        fields = '__all__'
    
class PatientForm(ModelForm):
    class Meta:
        model = Patient
        # exclude = ['race']
        fields = ['first_name',
                  'last_name',
                  'gender',
                  'dob',
                  'ethnicity',
                  'email',
                  'phone',
                  'address_type',
                  'street',
                  'zip_code',
                  'city',
                  'state']

    # TODO: Add race as a question
    #       Probably involves changing the model type

    gender = ChoiceField(choices=Gender.choices, widget=RadioSelect())
    # race = MultipleChoiceField(choices=Race.choices, widget=CheckboxSelectMultiple())
    ethnicity = ChoiceField(choices=Ethnicity.choices, widget=RadioSelect())
    # state = ChoiceField(choices=States.choices, widget=Select())
    address_type = ChoiceField(choices=AddressType.choices, widget=RadioSelect())