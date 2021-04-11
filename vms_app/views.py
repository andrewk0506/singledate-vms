from django.shortcuts import render
from vms_app.models import Staff

from .models import Dose


def index(request):
    return render(request, "index.html", {})


def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
    return render(request, "check.html", {})


def signup(request):
    return render(request, "signup.html", {})


def verify(request):
    return render(request, "verify.html", {})


def admin_login(request):
    return render(request, "admin-login.html")


def role_select(request):
    return render(request, "role-selection.html")


def staff_select(request):
    context = {"staff": Staff.objects.all()}
    # print("staff is", Staff.objects.first().surName)
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
