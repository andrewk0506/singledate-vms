from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from vms_app.forms import CreateStaffForm
from vms_app.models import Staff, Slot, Dose
from vms_app.dummydata import create_data, create2

from .models import Dose
from django.db import models
from vms_app.models import Patient
from vms_app.models import MedicalEligibilityAnswer, MedicalEligibilityQuestion
from .models import Slot
from vms_app.models.scheduling import Site
from vms_app.models.utils import Gender
from django.http import HttpResponseRedirect
from django.urls import reverse
import json

# from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Slot, Patient, Dose, Staff, Station, Patient, VaccineType, VaccineBatch

import pandas as pd

from .forms import PatientForm, MedicalEligibilityAnswerForm


def index(request):
    # TODO: figure out what site we're at, eg; leonia.getvaccinatednow.org
    context = {}
    site = Site.objects.first()  # TODO: Eventually won't be based on first but on actual clinic

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
    context = {}
    create_data()
    create2()
    # create object of form
    patient_form = PatientForm(request.POST or None)

    #
    medical_question = MedicalEligibilityQuestion.objects.all()
    questions = []
    for q in medical_question:
        new_question = {
            "prompt": q.question,
            "id": q.id,
            "explanation": q.explanation,
            "gender": q.gender
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
        ## Extract the questions and answer
        for q in medical_question:
            answer = MedicalEligibilityAnswer()
            answer.patient = patient
            answer.question = q
            answer.answered = now

            if q.bool:
                answer.answer_bool = True if patient_form.data[f'{q.id}'] == 'Yes' else False
            else:
                answer.answer_text = patient_form.data[f'{q.id}']

            answer.save()
        return HttpResponseRedirect("/registered")
    else:
        print(f"FORM IS NOT VALID\n\n{patient_form.data}")
        print(f"ERRORS: {patient_form.errors} \nNON FIELD ERRORS: {patient_form.non_field_errors()}")

    context = {
        'patient_form': patient_form,
        'medical_question': questions
    }

    return render(request, "signup.html", context)


def verify(request):
    """
    Handle request from the verify page: Query the database for the user submitted information
    and inform whether the user has been registered. If registered, say so; if not registered,
    point the user to the register page.
    """
    patients = Patient.objects.all()
    form = request.GET
    if (len(form) == 0):
        # First time visiting the verify page.
        return render(request, "verify.html", {})
    registered = False
    if "searchBy" in form:
        # Verify by email or phone.
        for p in patients:
            if form["searchBy"] == "email":
                if p.first_name == form["firstName"] and \
                        p.last_name == form["lastName"] and \
                        p.email == form["searchByOption"]:
                    registered = True
                    break
            else:
                if p.first_name == form["firstName"] and \
                        p.last_name == form["lastName"] and \
                        p.phone == form["searchByOption"]:
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


#
# @login_required(login_url="account_login")
# def export_data(request):
#     email = request.user.email
#     adminStaffAccounts = Staff.objects.filter(email=email)
#     adminRoles = []
#     for acct in adminStaffAccounts:
#         adminRoles.append(acct.role)
#
#
#     allowedSites = []
#     for role in adminRoles:
#         if role.role == "A":
#             allowedSites.append((role.site, str(role.site)))
#
#     context = {"allowedSites": allowedSites}
#     siteid = []
#     for site in context["allowedSites"]:
#         siteid.append(site[0].id)
#
#     return render(request, "export-data.html", context=context)


@login_required(login_url='account_login')
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
        return HttpResponseRedirect('appointments')
        # return render(request, "todays-appts.html")
        # return redirect("/vms/stations/appointments")


@login_required(login_url='account_login')
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


@login_required(login_url='account_login')
def patient_info(request):
    print(request.session)

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


@login_required(login_url='account_login')
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


@login_required(login_url='account_login')
def next_appt(request):
    return render(request, "nextappt.html")


@login_required(login_url='account_login')
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
            messages.success(request,
                             "{email} has been registered successfully".format(
                                 email=email
                             )
                             )

    context = {}
    return render(request, "staff-register.html", context)


def patient_matching():
    # first we need to figure out how many doses there are
    num_doses = 0
    # we are retrieving the set where it is a first dose and the patient id is null
    q = Dose.objects.filter(secondDose=0, patient_id=None)
    num_doses = q.count()

    # retrieves a queryset of patients of the size of the num_doses available
    patients = Patient.objects.all()[:num_doses]
    return patients


@login_required(login_url='account_login')
def export_data(request):
    # getting sites
    email = request.user.email
    adminStaffAccounts = Staff.objects.filter(email=email)
    adminRoles = []
    for acct in adminStaffAccounts:
        adminRoles.append(acct.role)

    allowedSites = []
    for role in adminRoles:
        if role.role == "A":
            allowedSites.append((role.site, str(role.site)))

    will_be_unique = Slot.objects.all()
    canuarray = [4, 5, 6]

    activateDates = []
    i = ""
    for i in will_be_unique:
        # making into calendar date
        caldate = datetime.strftime(i.startTime, "%d/%m/%Y")
        activateDates.append(caldate)
    # making ito default date form
    defaultDate = datetime.strftime(i.startTime, "%m/%d/%Y")

    context = {'canuarray': canuarray,
               'activateDates': activateDates,
               'defaultDate': defaultDate,
               "allowedSites": allowedSites}
    return render(request, 'export-data.html', context)


def create_csv(request):
    try:
        print("TRYING")
        print(request.POST)
        site = request.POST['site']
        selected_date = datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')

    except:
        print("CATCH!")
        # print(request.POST['datepicker'])
        # getting sites
        email = request.user.email
        adminStaffAccounts = Staff.objects.filter(email=email)
        adminRoles = []
        for acct in adminStaffAccounts:
            adminRoles.append(acct.role)

        allowedSites = []
        for role in adminRoles:
            if role.role == "A":
                allowedSites.append((role.site, str(role.site)))

        will_be_unique = Slot.objects.all()
        canuarray = [4, 5, 6]

        activateDates = []
        i = ""
        for i in will_be_unique:
            activateDates.append(datetime.strftime(i.startTime, "%d/%m/%Y"))
        defaultDate = datetime.strftime(i.startTime, "%m/%d/%Y")

        context = {'canuarray': canuarray,
                   'activateDates': activateDates,
                   'defaultDate': defaultDate,
                   "allowedSites": allowedSites}
        return render(request, 'dashboardreal.html', context)
    print(selected_date)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csvfile.csv"'

    def query_dash_data(date, site):
        """
        Returns data for dashboard
        :param date: datetime.date object, the date for which data is queried
        :param site: int, ID of site for which data is queried
        :return:  num_doses (number of doses dispensed as an int), station_doses (list of (station name, number of doses) tuples)
        """
        slots = Slot.objects.filter(startTime__startswith=date, site__id=site).values("id")
        dfSlot = pd.DataFrame(list(slots), columns=["id"])
        doses = Dose.objects.filter(slot__in=list(dfSlot["id"]))
        num_doses = len(doses)

        station_doses = []
        stations = Station.objects.filter(site__id=site).values("id", "stationName")
        dfStation = pd.DataFrame(list(stations), columns=["id", "stationName"])
        for station in stations:
            st_doses = Dose.objects.filter(station__id=station['id'])
            station_doses.append((station['stationName'], len(st_doses)))

        return num_doses, station_doses

    try:
        print("TRYING Dash if date")
        date_selected = datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')
        num_doses, station_doses = (query_dash_data(date_selected.date(), 1))
        print("num doses: " + str(num_doses))
        print("station doses: " + str(station_doses))
    except:
        print("CATCH Dash no date!")

    ## ADD TABLE QUERIES AND MAKE CSV
    strdate = datetime.strftime(selected_date, "%Y-%m-%d")
    qsDose = Dose.objects.filter(timeVax__startswith=strdate, ).order_by('patient').values("patient", "vaccine",
                                                                                           'administered',
                                                                                           "slot")  # TODO put in amount column from vaccinetype
    dfDose = pd.DataFrame(list(qsDose), columns=["patient", "vaccine", 'administered', "slot"])
    dfDose.rename(columns={"vaccine": "Vaccine Lot Number", "administered": "Vaccine Route of Administration"},
                  inplace=True)

    qsSlot = Slot.objects.filter(id__in=list(dfDose["slot"])).values("id", "site", "startTime", "duration",
                                                                     "vaccineType")
    for dicto in qsSlot:
        dicto['endTime'] = dicto['startTime'] + timedelta(minutes=+int(dicto['duration']))
        dicto['Date of Administration'] = dicto['startTime'].strftime("%Y%m%d")
    dfSlot = pd.DataFrame(list(qsSlot),
                          columns=["id", "site", "startTime", "endTime", "vaccineType", "Date of Administration"])
    df_Dose_Slot = pd.merge(dfDose, dfSlot, left_on="slot", right_on="id", how="left")
    df_Dose_Slot.rename(columns={"startTime": "Booking Start", "endTime": "Booking End", "site": "Site ID"},
                        inplace=True)
    df_Dose_Slot.drop(columns='id', inplace=True)

    qsPatient = Patient.objects.filter(person__in=list(df_Dose_Slot["patient"])).values("person", "first_name",
                                                                                        "last_name", "dob", "gender",
                                                                                        "race", "ethnicity", "phone",
                                                                                        "email", "street", "city",
                                                                                        "zip_code", "state",
                                                                                        "address_type")
    for dicto in qsPatient:
        dicto['DOB_Day'] = dicto["dob"].strftime("%d")
        dicto['DOB_Month'] = dicto["dob"].strftime("%m")
        dicto['DOB_Year'] = dicto["dob"].strftime("%Y")
    dfPatient = pd.DataFrame(list(qsPatient),
                             columns=["person", "first_name", "last_name", "DOB_Day", "DOB_Month", "DOB_Year", "gender",
                                      "race", "ethnicity", "phone", "email", "street", "city", "zip_code", "state",
                                      "address_type"])
    df_Dose_Slot_Patient = pd.merge(df_Dose_Slot, dfPatient, left_on="patient", right_on="person", how="left")
    df_Dose_Slot_Patient.rename(
        columns={"first_name": "Patient First Name", "last_name": "Patient Last Name", "gender": "Administrative Sex",
                 "ethnicity": "Ethnic Group", "street": "Street Address", "city": "City", "state": "State",
                 "zip_code": "Zip Code", "email": "Email Address", "phone": "Phone Number",
                 "address_type": "Patient Address Type", "race": "Race"}, inplace=True)
    df_Dose_Slot_Patient.drop(columns='person', inplace=True)

    qsVaccineType = VaccineType.objects.filter(id__in=list(df_Dose_Slot_Patient["vaccineType"])).values("id", "name",
                                                                                                        "amount")
    dfVaccineType = pd.DataFrame(list(qsVaccineType), columns=["id", "name", "amount"])

    df_Dose_Slot_Patient_VaccineType = pd.merge(df_Dose_Slot_Patient, dfVaccineType, left_on="vaccineType",
                                                right_on="id", how="left")
    df_Dose_Slot_Patient_VaccineType.drop(columns="id", inplace=True)
    df_Dose_Slot_Patient_VaccineType.rename(
        columns={"name": "Vaccine Manufacturer Name", "amount": "Vaccine Administered Amount"}, inplace=True)

    df_Dose_Slot_Patient_VaccineType.drop(columns=["slot", "vaccineType"], inplace=True)
    # df_Dose_Slot_Patient_VaccineType = df_Dose_Slot_Patient_VaccineType[["patient", "Site ID", "Booking Start", "Booking End", "Patient Last Name", "DOB_Day", "DOB_Month", "DOB_Year", "Administrative Sex", "Race", "Ethnic Group", "Street Address", "City", "State", "Zip Code", "Patient Address Type", "Phone Number", "Email Address", "Date of Administration", "Vaccine Administered Amount", "Vaccine Lot Number", "Vaccine Manufacturer Name", "Vaccine Route of Administration"]]

    qsAnswers = MedicalEligibilityAnswer.objects.all().values("patient", "question",
                                                              "answer_text")  # TODO figure out which questions will have bool answer, or like test if answer_bool isn't Null?
    dfAnswers = pd.DataFrame(list(qsAnswers), columns=["patient", "question", "answer_text"])
    qsQuestions = MedicalEligibilityQuestion.objects.all().values("id", "question")
    dfQuestions = pd.DataFrame(list(qsQuestions), columns=["id", "question"])
    df_Questions_Answers = pd.merge(dfAnswers, dfQuestions, left_on="question", right_on="id", how="left")
    df_Questions_Answers.drop(columns=["question_x", "id"], inplace=True)
    df_Questions_Answers = df_Questions_Answers.pivot(index="patient", columns="question_y", values="answer_text")
    # df_Questions_Answers = df_Questions_Answers[["Do you have a bleeding disorder or are you on medication that affects your immune system?", "Do you have any allergies to medication, and/or have you ever had an adverse reaction to a vaccine?", "Do you have a fever?", "Are you pregnant or do you plan to become pregnant soon?", "Are you currently breastfeeding?", "Have you received another COVID-19 vaccine?", "Have you had any OTHER vaccine in the last 14 days?", "Will you be available for your second dose in approximately 4 weeks?", "Comments"]]
    df_final = pd.merge(df_Dose_Slot_Patient_VaccineType, df_Questions_Answers, left_on="patient", right_on="patient",
                        how="left")
    df_final.drop(columns="patient", inplace=True)
    df_final = df_final[
        ["Site ID", "Booking Start", "Booking End", "Patient Last Name", "Patient First Name", "DOB_Day", "DOB_Month",
         "DOB_Year", "Administrative Sex", "Race", "Ethnic Group", "Street Address", "City", "State", "Zip Code",
         "Patient Address Type", "Phone Number", "Email Address",
         "Do You Have A Bleeding Disorder Or Are You On Medication That Affects Your Immune System?",
         "Do You Have Any Allergies To Medication, And/Or Have You Ever Had An Adverse Reaction To A Vaccine?",
         "Do You Have A Fever?", "Are You Pregnant Or Do You Plan To Become Pregnant Soon?",
         "Are You Currently Breastfeeding?", "Have You Received Another Covid-19 Vaccine?",
         "Have You Had Any Other Vaccine In The Last 14 Days?",
         "Will You Be Available For Your Second Dose In Approximately 4 Weeks?", "Comments", "Date of Administration",
         "Vaccine Administered Amount", "Vaccine Lot Number", "Vaccine Manufacturer Name",
         "Vaccine Route of Administration"]]

    df_final.to_csv(response)
    return response
