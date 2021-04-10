from django.forms import ModelForm
from .models.user import Staff

class CreateStaffForm(ModelForm):
	class Meta:
		model = Staff
		fields = '__all__'