from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from vms_app.models import Dose, Role, Staff, Site
from vms_app.forms import CreateStaffForm
from vms_app.decorators import admin_role_required



def index(request):
    return render(request, "index.html", {})


def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
	return render(request, "search.html", {})

def signup(request):
    return render(request, "signup.html", {})


@login_required(login_url="account_login")
def verify(request):
    return render(request, "verify.html", {})



@login_required(login_url="account_login")
def role_select(request):
    return render(request, "role-selection.html")

@login_required(login_url="account_login")
def export_data(request):
    email = request.user.email
    print("email of user is: ", email)
    adminStaffAccounts = Staff.objects.filter(email=email)
    adminRoles = []
    for acct in adminStaffAccounts:
        adminRoles.append(acct.role)


    allowedSites = []
    for role in adminRoles:
        print(role)
        if role.role == "A":
            allowedSites.append((role.site, str(role.site)))

    context = {"allowedSites": allowedSites}

    return render(request, "export-data.html", context=context)


@login_required(login_url='account_login')
def staff_select(request):
    request.session['role'] = 'VACCINATOR'
    allStaff = Staff.objects.all()
    context = {"staff": allStaff}
    for field in allStaff[0]._meta.fields:
        print("staff field", field.name)

    return render(request, "select-staff.html", context)


@login_required(login_url='account_login')
def appointments(request):
    return render(request, "todays-appts.html")


@login_required(login_url='account_login')
def patient_info(request):
    return render(request, "patient-info.html")


@login_required(login_url='account_login')
def medical_questions(request):
    return render(request, "medical-questions.html")


@login_required(login_url='account_login')
def next_appt(request):
    return render(request, "nextappt.html")


@login_required(login_url='account_login')
def vaccine_info(request):
    context = {"locations": Dose.LOCATIONS}
    return render(request, "vaccine-information.html", context)


@login_required(login_url='account_login')
def vaccine_info_submit(request):
    print(request.POST)
    return vaccine_info(request)


def register_new_staff(request):
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            messages.success(request,
                "{email} has been registered successfully".format(
                    email=email
                )
            )


    context = {}
    return render(request, "staff-register.html", context)
