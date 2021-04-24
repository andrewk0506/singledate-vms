from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vms_app.forms import CreateStaffForm, PatientForm
from vms_app.models import Staff, Slot, Dose

from vms_app.models import Patient
from vms_app.models import MedicalEligibilityAnswer, MedicalEligibilityQuestion
from vms_app.models.scheduling import Site
from django.http import HttpResponseRedirect
import datetime


def index(request):
    # TODO: figure out what site we're at, eg; leonia.getvaccinatednow.org
    context = {}
    site = (
        Site.objects.first()
    )  # TODO: Eventually won't be based on first but on actual clinic

    if site:
        context["siteDescription"] = site.comments
    return render(request, "preregister.html", context)


# Patient registration
def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
    return render(request, "search.html", {})


def signup(request):
    context = {}

    # create object of form
    patient_form = PatientForm(request.POST or None)

    medical_question = MedicalEligibilityQuestion.objects.all()
    questions = []
    for q in medical_question:
        new_question = {
            "prompt": q.question,
            "id": q.id,
            "explanation": q.explanation,
            "gender": q.gender,
        }
        if q.bool:
            additional = {"type": "select", "options": ["No", "Yes"]}
        else:
            additional = {"type": "text", "options": 100}

        questions.append(dict(new_question, **additional))

    # check if form data is valid
    if patient_form.is_valid():
        # save the form data to model
        patient = patient_form.save()
        now = datetime.datetime.now()
        print(f"FORM IS VALID\n\n{patient_form.data}")
        # Extract the questions and answer
        for q in medical_question:
            answer = MedicalEligibilityAnswer()
            answer.patient = patient
            answer.question = q
            answer.answered = now

            if q.bool:
                answer.answer_bool = (
                    True if patient_form.data[f"{q.id}"] == "Yes" else False
                )
            else:
                answer.answer_text = patient_form.data[f"{q.id}"]

            answer.save()
        return HttpResponseRedirect("/registered")
    else:
        print(f"FORM IS NOT VALID\n\n{patient_form.data}")
        print(
            f"ERRORS: {patient_form.errors} \
            NON FIELD ERRORS: {patient_form.non_field_errors()}"
        )

    context = {"patient_form": patient_form, "medical_question": questions}

    return render(request, "signup.html", context)


def verify(request):
    """
    Handle request from the verify page: Query the database for the
    user submitted information and inform whether the user has been registered.
    If registered, say so; if not, point the user to the register page.
    """
    patients = Patient.objects.all()
    form = request.GET
    if len(form) == 0:
        # First time visiting the verify page.
        return render(request, "verify.html", {})
    registered = False
    if "searchBy" in form:
        # Verify by email or phone.
        for p in patients:
            if form["searchBy"] == "email":
                if (
                    p.first_name == form["firstName"]
                    and p.last_name == form["lastName"]
                    and p.email == form["searchByOption"]
                ):
                    registered = True
                    break
            else:
                if (
                    p.first_name == form["firstName"]
                    and p.last_name == form["lastName"]
                    and p.phone == form["searchByOption"]
                ):
                    registered = True
                    break
    else:
        # Verify by reference code.
        for p in patients:
            if str(p.person) == form["referenceCode"]:
                registered = True
                break
    context = {"registered": registered, "show_verify_result": True}
    return render(request, "verify.html", context)


# Admin
def registered(request):
    return render(request, "registered.html", {})


@login_required(login_url="account_login")
def role_select(request):
    return render(request, "role-selection.html")


@login_required(login_url="account_login")
def export_data(request):
    email = request.user.email
    adminStaffAccounts = Staff.objects.filter(email=email)
    adminRoles = []
    for acct in adminStaffAccounts:
        adminRoles.append(acct.role)

    allowedSites = []
    for role in adminRoles:
        if role.role == "A":
            allowedSites.append((role.site, str(role.site)))

    context = {"allowedSites": allowedSites}

    return render(request, "export-data.html", context=context)


@login_required(login_url="account_login")
def staff_select(request):
    if request.method == "GET":
        context = {"staff": Staff.objects.all()}
        return render(request, "select-staff.html", context)

    elif request.method == "POST":
        print("post request is", request.POST)
        print("redirecting...")
        post_request = request.POST
        vaccinator = post_request["vaccinator"]
        support = post_request["staff-member"]
        request.session["vaccinator"] = vaccinator
        request.session["staff-member"] = support
        return HttpResponseRedirect("appointments")
        # return render(request, "todays-appts.html")
        # return redirect("/vms/stations/appointments")


@login_required(login_url="account_login")
def appointments(request):
    if request.method == "GET":
        print("current session is", request.session.items())
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        print("now is ", now)

        slots = Slot.objects.filter(startTime__lte=now)

        context = {"appointments": slots}
        return render(request, "todays-appts.html", context)


@login_required(login_url="account_login")
def patient_info(request):
    if request.method == "GET":
        # Get the patient ID from the form
        patient_id = Patient.objects.first().person
        if request.POST and request.POST["patient_id"]:
            patient_id = request.POST["patient_id"]

        # Populate the session
        print("Session: ", request.session.items())
        if not request.session.get("station_management", None):
            request.session["station_management"] = {}
        request.session["station_management"]["patient_id"] = patient_id

        # Obtain the patient object
        patient = Patient.objects.filter(person=patient_id).first

        if not patient:
            context = {"patient": patient}

        return render(request, "patient-info.html", context)
    elif request.method == "POST":
        # set whatever is required into session
        # then redirect to the next page
        return redirect("/vms/stations/medical_questions")


@login_required(login_url="account_login")
def medical_questions(request):
    # This is a redirect from patient_info.
    #
    # Session should contain patient_id, which can be used
    # to fetch and display the medical-questions & answers.
    #
    # On button submission, we catch the POST request here
    # and either we update the DB right away, or we set the
    # questions and answers in the session again and
    # redirect it to the next page (just like patient_info).

    if request.method == "GET":
        # if session is not set, redirect to the
        # appointments page, as directly landing here is not allowed.
        # rs = request.session
        # if not rs or not rs.get("station_management", None):
        #    return redirect("/vms/stations/appointments")

        # Note that I temporarily commented the above lines (82-84) out
        # so that it is possible to directly access and test this single
        # page without being redirected to /vms/stations/appointments.

        context = {"medical": MedicalEligibilityQuestion.objects.all()}
        return render(request, "medical-questions.html", context)
    elif request.method == "POST":
        return redirect("/vms/stations/next_appt")


@login_required(login_url="account_login")
def next_appt(request):
    return render(request, "nextappt.html")


@login_required(login_url="account_login")
def vaccine_info(request):
    if request.method == "GET":
        # if session is not set, redirect to the
        # appointments page, as directly landing here is not allowed.
        rs = request.session
        if not rs or not rs.get("station_management", None):
            return redirect("/vms/stations/appointments")
        context = {"locations": Dose.LOCATIONS}
        return render(request, "vaccine-information.html", context)
    elif request.method == "POST":
        # Update the session object by filling in the page's data
        print("the form request is", request.POST)
        vaccine_info_page_data = {
            "method": request.POST["page-form-administration-method"],
            "location": request.POST["page-form-administration-area"],
            "notes": request.POST["page-form-notes"],
        }
        request.session["station_management"][
            "page-vaccine-info"
        ] = vaccine_info_page_data

        # Send the entire session object for updating the DB
        process_request(dict(request.session["station_management"]))

        # If processing is successful, reset the session
        del request.session["station_management"]

        # Then redirect
        # Note, the UI currently ignores this redirect and
        # lets the station staff choose to redirect or not
        # from the UI.
        return redirect("/vms/stations/appointments")


# Maybe all these processing methods
# below can be moves somewhere else.

# Method to update all the tables
# for each page data inside the
# session data.
#
# session_data = {
#   "page-medical-questions": {...},
#   "page-next-appts": {...},
#   "page-vaccine-info": {...}
# }
def process_request(session_data):
    # print("Session data: ", session_data)
    patient_id = session_data.get("patient_id", 0)
    page_vaccine_info = session_data.get("page-vaccine-info", None)
    process_vaccine_info_data(patient_id, page_vaccine_info)


def process_vaccine_info_data(patient_id, data):
    if data is None:
        return

    # Update vaccine info
    dose = Dose.objects.filter(patient_id=patient_id).first()
    if dose is not None:
        dose.notes = data.get("notes", None)
        dose.location = data.get("location", None)
        dose.save()


def register_new_staff(request):
    if request.method == "POST":
        form = CreateStaffForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            message_str = "{email} has been registered successfully".format(email=email)
            messages.success(request, message_str)

    context = {}
    return render(request, "staff-register.html", context)


def patient_matching():
    q = Dose.objects.filter(secondDose=0, patient_id=None)
    num_doses = q.count()

    # retrieves a queryset of patients of the size of the num_doses available
    patients = Patient.objects.all()[:num_doses]
    return patients
