from django.shortcuts import render, redirect
from vms_app.models import Staff

from .models import Dose
from .models.user import Patient as Patient


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
    return render(request, "select-staff.html", context)


def appointments(request):
    return render(request, "todays-appts.html")


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
        context = {"patient": patient}
        return render(request, "patient-info.html", context)
    elif request.method == "POST":
        # set whatever is required into session
        # then redirect to the next page
        return redirect("/vms/stations/medical_questions")


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
        rs = request.session
        if not rs or not rs.get("station_management", None):
            return redirect("/vms/stations/appointments")
        return render(request, "medical-questions.html")
    elif request.method == "POST":
        return redirect("/vms/stations/next_appt")


def next_appt(request):
    return render(request, "nextappt.html")


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
    print("Session data: ", session_data)
    process_vaccine_info_data(session_data.get("page-vaccine-info", None))


def process_vaccine_info_data(data):
    if data is None:
        return

    # Update vaccine info
    dose = Dose.objects.filter(patient=data.get("patient_id", 0)).first()
    if dose is not None:
        dose.notes = data.get("notes", None)
        dose.location = data.get("location", None)
        dose.save()
