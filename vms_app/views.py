from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vms_app.models import Staff

from .models import Dose


def index(request):
    return render(request, "index.html", {})


def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
	return render(request, "search.html", {})

def signup(request):
    return render(request, "signup.html", {})


def verify(request):
    return render(request, "verify.html", {})


def admin_login(request):
    print("In admin_login again")
    if request.user.is_authenticated:
        print("User is authentiated. Redirecting to role select")
        return redirect('role-select')

    else:
        if request.method == "POST":
            print("request.POST is: ", request.POST)
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = None
            try:
                user = authenticate(request, username=email, password=password)
            except Exception as e:
                print (e)

            if user is not None:
                print("user is not none!")
                login(request, user)
                return redirect('role-select')
            else:
                messages.info(request, 'Email or password is incorrect')

            print("email is: ", email)
        else:
            print("request.method is: ", request.method)


    context = {}
    return render(request, "admin-login.html", context)


@login_required(login_url='admin-login')
def role_select(request):
    return render(request, "role-selection.html")


@login_required(login_url='admin-login')
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
