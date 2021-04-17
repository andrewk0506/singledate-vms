from django.shortcuts import render, redirect
from vms_app.models import Staff

from .models import Dose
from django.db import models
from vms_app.models import Patient
from vms_app.models import MedicalEligibilityAnswer, MedicalEligibilityQuestion
from .models import Slot
from vms_app.models.scheduling import Site
from vms_app.models.utils import Gender
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
import json

from .forms import PatientForm, MedicalEligibilityAnswerForm

def index(request):
    # TODO: figure out what site we're at, eg; leonia.getvaccinatednow.org 
    context={}
    site = Site.objects.first() # TODO: Eventually won't be based on first but on actual clinic

    context["siteDescription"] = site.comments
    return render(request, "preregister.html", context)


# def preregister(request):
#     return render(request, "preregister.html", {})


# Patient registration
def preregister(request):
    return render(request, "preregister.html", {})


def check(request):
    return render(request, "search.html", {})


def signup(request):
    """
        TODO: 
            6. Populate Answer with answer from table 

        DONE: 
            1. Reconnect basic info name, etc...
            2. Connect contact info/address etc...
            3. Submit those to db
            4. New page 
            5. Populate Question with db



    """
    context = {}
    # questionData = json.loads(open("vms_app/templates/json/questions.json", "r").read())

    # create object of form
    patient_form = PatientForm(request.POST or None)
    answer_form = MedicalEligibilityAnswerForm(request.POST or None)

    # check if form data is valid
    if patient_form.is_valid():
        # save the form data to model
        print(f"FORM IS VALID\n\n{patient_form.data}")
        patient_form.save()
        return HttpResponseRedirect("/registered")
    else:
        print(f"FORM IS NOT VALID\n\n{patient_form.data}")

    if request.method == "GET":
        medQuestions = MedicalEligibilityQuestion.objects.all()
        medPage = {"questions": []}
        for medQ in medQuestions:
            print(medQ.question)
            newQuestion = {
                "prompt": medQ.question,
                "id": medQ.id,
                "explanation": medQ.explanation,
                "gender": medQ.gender
            }
            if medQ.bool:
                additional = {"type": "select", "options": ["No", "Yes"]}
            else:
                additional = {"type": "text", "options": 100}

            medPage["questions"].append(dict(newQuestion, **additional))

    context = {
        'patient_form': patient_form,
        'answer_form': answer_form,
        'questionData': medPage
    }

    print(context['questionData'])

    return render(request, "signup.html", context)


def verify(request):
    return render(request, "verify.html", {})


# Admin
def registered(request):
    return render(request, "registered.html", {})


def admin_login(request):
    return render(request, "admin-login.html")


def role_select(request):
    return render(request, "role-selection.html")


def staff_select(request):
    if request.method == "GET":
        # print("staff is", Staff.objects.first())
        context = {"staff": Staff.objects.all()}

        # print("staff is", Staff.objects.first().surName)
        return render(request, "select-staff.html", context)

    elif request.method == "POST":
        print("post request is", request.POST)
        print("redirecting...")
        post_request = request.POST
        vaccinator = post_request["vaccinator"]
        support = post_request["staff-member"]
        request.session["vaccinator"] = vaccinator
        request.session["staff-member"] = support
        return HttpResponseRedirect('appointments')
        # return render(request, "todays-appts.html")
        # return redirect("/vms/stations/appointments")


def appointments(request):
    if request.method == "GET":
        print("current session is", request.session.items())
        now = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        print("now is ", now)

        # get all slots within a few hours
        slots = Slot.objects.filter(startTime__lte=now)

        # get all doses
        dose = Dose.objects.filter(slot__in=slots)
        # dose_ids = dose.patient_id

        patients = Patient.objects.filter(person__in=dose)
        # print("slots are", slots[0].capacity)
        # print("doses are", dose[0].location)
        # print("patients are", patients[0].first_name)
        context = {"appointments": slots}
        return render(request, "todays-appts.html", context)


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

        if patient != None:
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


def patient_matching():
    # first we need to figure out how many doses there are
    num_doses = 0
    # we are retrieving the set where it is a first dose and the patient id is null
    q = Dose.objects.filter(secondDose=0, patient_id=None)
    num_doses = q.count()

    # retrieves a queryset of patients of the size of the num_doses available
    patients = Patient.objects.all()[:num_doses]
    return patients
