from django.forms import ModelForm, ModelChoiceField, ChoiceField, RadioSelect, MultipleChoiceField, CheckboxSelectMultiple, Select, ValidationError
from .models import MedicalEligibilityAnswer, Patient
from .models.utils import Gender, Ethnicity, AddressType, States, Race
from phone_field.forms import PhoneFormField


# from formtools.wizard.views import SessionWizardView
# from django.shortcuts import render


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
                  'race',
                  'ethnicity',
                  'email',
                  'phone',
                  'address_type',
                  'street',
                  'zip_code',
                  'city',
                  'state']
        fieldsets = (
            ('Personal Details', {
                'fields': ('first_name',
                  'last_name',
                  'gender',
                  'dob',
                  'race',
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

    gender = ChoiceField(choices=Gender.choices, widget=RadioSelect())
    race = MultipleChoiceField(choices=Race.choices, widget=CheckboxSelectMultiple())
    ethnicity = ChoiceField(choices=Ethnicity.choices, widget=RadioSelect())
    state = ChoiceField(choices=States.choices, widget=Select())
    address_type = ChoiceField(choices=AddressType.choices, widget=RadioSelect())
    phone = PhoneFormField(required=False)


    def clean(self):
        cleaned_data = super(PatientForm, self).clean()
        new_patient_dob = cleaned_data.get("dob")
        new_patient_email = cleaned_data.get("email")
        new_patient_phone = cleaned_data.get("phone")

        # Check 1 
        c1 = Patient.objects.filter(dob=new_patient_dob).filter(email=new_patient_email).exists()
        # Check 2 
        c2 = Patient.objects.filter(dob=new_patient_dob).filter(phone=new_patient_phone).exists()
        print(f"Check results: {c1} / {c2}")

        if c1 or c2:
            raise ValidationError("This appears to be a duplicate registration!")


# class FormWizardView(SessionWizardView):
#     template_name = "path/to/template"
#     form_list = [PatientForm, MedicalEligibilityAnswerForm]

#     def done(self, form_list, **kwargs):
#         return render(self.request, 'done.html', {
#             'form_data': [form.cleaned_data for form in form_list],
#         })


