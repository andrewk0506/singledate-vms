from django.forms import ModelForm, ModelChoiceField, ChoiceField, RadioSelect, MultipleChoiceField, CheckboxSelectMultiple, Select
from django import forms
from .models.user import Staff
from .models import MedicalEligibilityAnswer, Patient, Role
from .models.utils import Gender, Ethnicity, AddressType
from phone_field import PhoneField

class CreateStaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ["first_name", "last_name",  "email", "phone_number", "HIPAACert", "medical_id"]


class MedicalEligibilityAnswerForm(ModelForm):
    class Meta:
        model = MedicalEligibilityAnswer
        fields = '__all__'

class PatientForm(ModelForm):
    class Meta:
        model = Patient
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
                # exclude = ['race']
        fieldsets = (
            ('Personal Details', {
                'fields': ('first_name',
                  'last_name',
                  'gender',
                  'dob',
                  'ethnicity')
            }),
            ('Contact Information', {
                'fields': ('email',
                  'phone',
                  'address_type',
                  'street',
                  'zip_code',
                  'city',
                  'state')
            })
        )

    # TODO: Add race as a question
    #       Probably involves changing the model type

    gender = ChoiceField(choices=Gender.choices, widget=RadioSelect())
    # race = MultipleChoiceField(choices=Race.choices, widget=CheckboxSelectMultiple())
    ethnicity = ChoiceField(choices=Ethnicity.choices, widget=RadioSelect())
    # state = ChoiceField(choices=States.choices, widget=Select())
    address_type = ChoiceField(choices=AddressType.choices, widget=RadioSelect())



# class FormWizardView(SessionWizardView):
#     template_name = "path/to/template"
#     form_list = [PatientForm, MedicalEligibilityAnswerForm]

#     def done(self, form_list, **kwargs):
#         return render(self.request, 'done.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })
