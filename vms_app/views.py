from django.shortcuts import render
from vms_app.models import Staff

from .models import Dose
from .models.user import PatientForm


def index(request):
    return render(request, "index.html", {})


# Patient registration
def preregister(request):
    return render(request, "preregister.html", {})

def check(request):
	return render(request, "search.html", {})

def signup(request):
    context ={}
  
    # create object of form
    form = PatientForm(request.POST or None)
      
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        print(f"FORM IS VALID\n\n{form.data}")
        form.save()
    else:
        print(f"FORM IS NOT VALID\n\n{form.data}")
  
    context['form']= form
    return render(request, "signup.html", context)

def verify(request):
    return render(request, "verify.html", {})


# Admin
def admin_login(request):
    return render(request, "admin-login.html")


def role_select(request):
    return render(request, "role-selection.html")


def staff_select(request):
    context = {"staff": Staff.objects.all()}
    return render(request, "select-staff.html", context)


def appointments(request):
    return render(request, "todays-appts.html")


def patient_info(request):
    return render(request, "patient-info.html")


def medical_questions(request):
    return render(request, "medical-questions.html")


def next_appt(request):
    return render(request, "nextappt.html")


def vaccine_info(request):
    context = {"locations": Dose.LOCATIONS}
    return render(request, "vaccine-information.html", context)


def vaccine_info_submit(request):
    print(request.POST)
    return vaccine_info(request)
