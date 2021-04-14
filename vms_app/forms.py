from django import forms
from .models.user import Staff
from .models import Role
from phone_field import PhoneField

class CreateStaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ["first_name", "last_name",  "email", "phone_number", "HIPAACert", "medical_id"]
