from django import forms
from .models.user import Staff
from .models import Role
from phone_field import PhoneField

def getRoleChoices():
    roleIdNameMap = {}
    for rId, rLabel in Role.ROLES:
        roleIdNameMap[rId] = rLabel

    roles = Role.objects.all()
    roleChoices = []
    for role in roles:
        site = role.site
        rollName = "ROLE: {role} -- SITE: {street}, {city}, {state} - {zipcode}".format(
            role=roleIdNameMap[role.role],
            street=site.street,
            city=site.city,
            state=site.state,
            zipcode=site.zipCode
        )
        roleChoices.append((role.id, rollName))


    return roleChoices


class CreateStaffForm(forms.ModelForm):
	class Meta:
		model = Staff
		fields = ["first_name", "last_name",  "email", "phone_number", "HIPAACert", "medical_id"]

class LoginForm(forms.Form):

    def login(self, request, user):
        request.session['role'] = 'ADMIN'


class SignupForm(forms.Form):
    last_name = forms.CharField(max_length=100, label='Last Name')
    first_name = forms.CharField(max_length=100, label='First Name')
    phone_number = forms.CharField(max_length=12, required=False)
    HIPAACert = forms.DateField(label="HIPAACert", widget=forms.SelectDateWidget)
    medical_id = forms.IntegerField(label='Medical ID')
    roleId = forms.ChoiceField(choices=getRoleChoices(), label='Role')


    def signup(self, request, user):
        roleId = self.cleaned_data['roleId']
        role = Role.objects.get(id=roleId)
        staff = Staff.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            phone_number=self.cleaned_data['phone_number'],
            HIPAACert=self.cleaned_data['HIPAACert'],
            medical_id=self.cleaned_data['medical_id'],
            role=role
        )
        user.profile = staff
        user.save()
        print("printing user", user)
        print("printing profile`", user.profile)
        print("printing profile.role", user.profile.role)
