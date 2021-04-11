from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from vms_app.models import Dose, Role, Staff
from vms_app.forms import CreateStaffForm
from vms_app.decorators import admin_login_required, has_group



def index(request):
    return render(request, "index.html", {})


def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
	return render(request, "search.html", {})

def signup(request):
    return render(request, "signup.html", {})


@login_required
def verify(request):
    return render(request, "verify.html", {})

def admin_logout(request):
    if request.session.has_key("role"):
        print("Role before logout is: ", request.session['role'])
        del request.session["role"]
    logout(request)

    return redirect("admin-login")


def admin_login(request):
    print("In admin_login again")
    print("request.METHOD is: ", request.method)
    if request.method == "GET" and request.user.is_authenticated and \
            has_group(request.user, "ADMIN"):
        print("user is authenticated currently")

        if request.session.has_key("role") and request.session["role"] != "ADMIN":
            context = { "message": "You need to login again to see this page" }
            return render(request, "admin-login.html", context)
        else:
            request.session["role"] = "ADMIN"
            return render(request, "role-select.html", {})

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
            request.session["role"] = "ADMIN"
            login(request, user)
            print("Authenticated user: {email} successfully.".format(email=email))
            return redirect('role-select')
        else:
            messages.info(request, 'Email or password is incorrect')

    context = {}
    return render(request, "admin-login.html", context)


@login_required(login_url='admin-login')
def role_select(request):
    return render(request, "role-selection.html")


@login_required(login_url='admin-login')
def staff_select(request):
    request.session['role'] = 'VACCINATOR'
    context = {"staff": Staff.objects.all()}
    return render(request, "select-staff.html", context)


@login_required(login_url='admin-login')
def appointments(request):
    return render(request, "todays-appts.html")


@login_required(login_url='admin-login')
def patient_info(request):
    return render(request, "patient-info.html")


@login_required(login_url='admin-login')
def medical_questions(request):
    return render(request, "medical-questions.html")


@login_required(login_url='admin-login')
def next_appt(request):
    return render(request, "nextappt.html")


@login_required(login_url='admin-login')
def vaccine_info(request):
    context = {"locations": Dose.LOCATIONS}
    return render(request, "vaccine-information.html", context)


@login_required(login_url='admin-login')
def vaccine_info_submit(request):
    print(request.POST)
    return vaccine_info(request)

@admin_login_required
def register_new_staff(request):
    if request.method == "POST":
        print("POST Data is: ", request.POST)
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            print("cleaned data is: ", form.cleaned_data)
            form.save()
            fname = form.cleaned_data.get('first_name')
            lname = form.cleaned_data.get('last_name')
            roleLabel = form.cleaned_data.get('role')
            messages.success(request,
                    "{fname} {lname} has been added as a new {role}".format(
                    fname=fname, lname=lname, role=roleLabel
                    )
            )

        else:
            print("Form errors are ", form.errors)

    roles = reversed(list(map(lambda x: x[1], Role.ROLES)))
    context = {"roles": roles}
    print("roles are: ", roles)
    print("Context is ", context)

    return render(request, "staff-register.html", context)



