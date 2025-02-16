#from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic

from .models import Slot, Person,Dose, Station, Patient, VaccineType, VaccineBatch, MedicalEligibilityAnswer, MedicalEligibilityQuestion
from djqscsv import write_csv
from djqscsv import render_to_csv_response
from .dummydata import create_dummydata


import pandas as pd

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     template = loader.get_template('vaccine/index.html')
#     context = {
#         'latest_question_list': latest_question_list,
#     }
#     return HttpResponse(template.render(context, request))

## HARD WAY FIRST TUTORIAL VERSION

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'vaccine/index.html', context)
#     #render(request object, template name, context)
#
# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'vaccine/detail.html', {'question': question})
# # def detail(request, question_id):
# #     try:
# #         question = Question.objects.get(pk=question_id)
# #     except Question.DoesNotExist:
# #         raise Http404("Question does not exist")
# #     return render(request, 'vaccine/detail.html', {'question': question})
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'vaccine/results.html', {'question': question})

##DJANGO GENERICS
class IndexView(generic.ListView):
    template_name = 'vaccine/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Slot.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Slot
    template_name = 'vaccine/detail.html'


class ResultsView(generic.DetailView):
    model = Slot
    template_name = 'vaccine/results.html'

def vote(request, question_id):
    print(request.POST['select'])
    print(request.POST['datepicker'])
    print(request.POST['datepicker2'])
    # question = get_object_or_404(Question, pk=question_id)
    # See if object exists that is selected
    # try:
    #     selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #     print(request.POST[''])
    #
    # except (KeyError, Choice.DoesNotExist):
    #     # Redisplay the question voting form.
    #     return render(request, 'vaccine/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
    # else:
    #     selected_choice.votes += 1
    #     selected_choice.save()
    #     # Always return an HttpResponseRedirect after successfully dealing
    #     # with POST data. This prevents data from being posted twice if a
    #     # user hits the Back button.
    #     return HttpResponseRedirect(reverse('vaccine:results', args=(question.id,)))
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'vaccine/results.html', {'question': question})
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'vaccine/results.html', {'question': question})
def happy(request):
    # create_dummydata()
    return render(request, 'vaccine/happy.html')

def daterange(request):
    try:
        print("TRYING")
        datetime.datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')
    except:
        return render(request, 'vaccine/dashboard2.html', {
            # 'error_message': "Select date",
        })
    try:
        print(request.POST['datepicker'])
        one = request.POST['datepicker']
        # print(request.POST['datepicker2'])
        #two = request.POST['datepicker2']
        one = datetime.datetime.strptime(one, '%m/%d/%Y')
        # two = datetime.datetime.strptime(two,'%m/%d/%Y')
    except (KeyError):
    # # Redisplay the question voting form.
        return render(request, 'vaccine/dashboard2.html', {
            'error_message': "Please select dates from the calendar options.",
        })
        print("no selection yet")

    def filterData(dateStart, dateEnd):
        filteredOnRange = Personmini.objects.filter(
        datevaccinatednumone__range=[dateStart,dateEnd]
        )
        return filteredOnRange

    def makeDate(datetimeobj):
        x = str(datetimeobj.year) + '-'
        if (len(str(datetimeobj.month)) == 1):
            x = x + '0' + str(datetimeobj.month) + '-'
        else:
            x = x + str(datetimeobj.month) + '-'
        if (len(str(datetimeobj.day)) == 1):
            x = x + '0' + str(datetimeobj.day)
        else:
            x = x + str(datetimeobj.day)
        return x

    def filterDate(date):
        # print(type(date))
        print("filter Date")
        print(makeDate(date))
        x = makeDate(date)
        # x = datetime.datetime.strptime(date, '%m/%d/%Y')

        # filteredDate = Personmini.objects.filter(datevaccinatednumone__date=date.year)
        # return filteredDate
        filteredDate = Personmini.objects.filter(datevaccinatednumone__startswith=x)
        return filteredDate




    # vaccinated_people = filterData(one, two)
    # print(makeDate(one))
    vaccinated_people = filterDate(one)
    ## ADD TABLE QUERIES AND MAKE CSV
    print(vaccinated_people)
    # error_message = " "
    # context = {'error_message': error_message}
    with open('vaccinated_data.csv', 'wb') as csv_file:
        write_csv(vaccinated_people, csv_file)
    return render_to_csv_response(vaccinated_people)
    # return render(request, 'vaccine/dateRange.html')

def dashboard(request):
    # print(request.POST['datepicker'])
    # print(request.POST['datepicker2'])
    latest_question_list = Question.objects.order_by('-pub_date')[:3]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'vaccine/dashboard.html', context)

def dashboard2(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:3]
    def makeDateCal(datetimeobj):
        x = ""
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        x = x + str(datetimeobj.year)
        return x
    def makeDefaultDate(datetimeobj):
        x = ""
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        x = x + str(datetimeobj.year)
        return x

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

    # try:
    # print(request.POST['datepicker'])
    will_be_unique = Personmini.objects.all()
    canuarray = [4,5,6]

    activateDates = []
    i = ""
    for i in will_be_unique:
        # print(i.datevaccinatednumone)
        # #convert to day/month/year
        # print(i.datevaccinatednumone.day)
        activateDates.append(makeDateCal(i.datevaccinatednumone))
    # print(activateDates)
    defaultDate = makeDefaultDate(i.datevaccinatednumone)



    context = {'latest_question_list': latest_question_list,
               'canuarray': canuarray,
               'activateDates':activateDates,
               'defaultDate':defaultDate}
    return render(request, 'vaccine/dashboard2.html',context)
# def lengths_barplot(request, analysis_id):
#     data = Lengths.objects.filter(analysis_id=analysis_id)
#     df = pd.DataFrame.from_records(data.values())
#     chart = alt.Chart(df).mark_bar().encode(
#         x=alt.X('length'),
#         y=alt.Y('count'),
#         color='type',
#         facet=alt.Facet('type', columns=1),
#     ).properties(
#         width=800
#     )
#     return HttpResponse(chart.to_json(), content_type='application/json')



def dashboardreal(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:3]
    def makeDateCal(datetimeobj):
        x = ""
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        x = x + str(datetimeobj.year)
        return x
    def makeDefaultDate(datetimeobj):
        x = ""
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        x = x + str(datetimeobj.year)
        return x

    # try:
    # print(request.POST['datepicker'])

    will_be_unique = Slot.objects.all()
    canuarray = [4,5,6]

    activateDates = []
    i = ""
    for i in will_be_unique:
        # print(i.startTime)
        # #convert to day/month/year
        # print(i.startTime.day)
        activateDates.append(makeDateCal(i.startTime))
    # print(activateDates)
    defaultDate = makeDefaultDate(i.startTime)



    context = {'canuarray': canuarray,
               'activateDates':activateDates,
               'defaultDate':defaultDate}
    return render(request, 'vaccine/dashboardreal.html',context)


def daterangereal(request):
    def makeDateCal(datetimeobj):
        x = ""
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        x = x + str(datetimeobj.year)
        return x
    def makeDefaultDate(datetimeobj):
        x = ""
        if (len(str(datetimeobj.month)) == 1):
            x = x + "0" + str(datetimeobj.month) + "/"
        else:
            x = x + str(datetimeobj.month) + "/"
        if (len(str(datetimeobj.day)) == 1):
            x = "0" + str(datetimeobj.day) + "/"
        else:
            x = x + str(datetimeobj.day) + "/"
        x = x + str(datetimeobj.year)
        return x

    try:
        print("TRYING")
        x = datetime.datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')
    except:
        print("CATCH!")
        # print(request.POST['datepicker'])

        will_be_unique = Slot.objects.all()
        canuarray = [4, 5, 6]

        activateDates = []
        i = ""
        for i in will_be_unique:
            # print(i.startTime)
            # # convert to day/month/year
            # print(i.startTime.day)
            activateDates.append(makeDateCal(i.startTime))
        # print(activateDates)
        defaultDate = makeDefaultDate(i.startTime)

        context = {'canuarray': canuarray,
                   'activateDates': activateDates,
                   'defaultDate': defaultDate}
        return render(request, 'vaccine/dashboardreal.html', context)
    print(x)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="csvfile.csv"'

    def makeDate(datetimeobj):
        x = str(datetimeobj.year) + '-'
        if (len(str(datetimeobj.month)) == 1):
            x = x + '0' + str(datetimeobj.month) + '-'
        else:
            x = x + str(datetimeobj.month) + '-'
        if (len(str(datetimeobj.day)) == 1):
            x = x + '0' + str(datetimeobj.day)
        else:
            x = x + str(datetimeobj.day)
        return x

    def filterDate(date):
        # print(type(date))
        print("filter Date")
        print(makeDate(date))
        x = makeDate(date)
        # x = datetime.datetime.strptime(date, '%m/%d/%Y')

        # filteredDate = Personmini.objects.filter(datevaccinatednumone__date=date.year)
        # return filteredDate
        # filteredDate = Slot.objects.filter(startTime__startswith=x).values("id", "site", "startTime", "duration", 'capacity', "vaccineType")
        filteredDate = Dose.objects.filter(timeVax__startswith=x).order_by('patient').values("patient", "vaccine",
                                                                                           "amount", 'administered',
                                                                                           "slot")
        return filteredDate

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
        x = datetime.datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')
        num_doses, station_doses = (query_dash_data(x.date(), 1))
        print("num doses: " + str(num_doses))
        print("station doses: " + str(station_doses))
    except:
        print("CATCH Dash no date!")



    # qsSlot = filterDate(x)
    qsDose = filterDate(x)
    ## ADD TABLE QUERIES AND MAKE CSV
    # print(qsSlot)


    dfDose = pd.DataFrame(list(qsDose), columns=["patient", "vaccine", "amount", 'administered', "slot"])
    dfDose.rename(columns={"vaccine": "Vaccine Lot Number", "administered": "Vaccine Route of Administration", "amount":"Vaccine Administered Amount"}, inplace=True)

    qsSlot = Slot.objects.filter(id__in=list(dfDose["slot"])).values("id", "site", "startTime", "duration", "vaccineType")
    for dicto in qsSlot:
        dicto['endTime'] = dicto['startTime'] + datetime.timedelta(minutes=+int(dicto['duration']))
        dicto['Date of Administration'] = dicto['startTime'].strftime("%Y%m%d")
    dfSlot = pd.DataFrame(list(qsSlot), columns=["id", "site", "startTime", "endTime", "vaccineType", "Date of Administration"])
    df_Dose_Slot = pd.merge(dfDose, dfSlot, left_on="slot", right_on="id", how="left")
    df_Dose_Slot.rename(columns={"startTime":"Booking Start", "endTime":"Booking End", "site":"Site ID"}, inplace=True)
    df_Dose_Slot.drop(columns='id', inplace=True)

    qsPatient = Patient.objects.filter(person__in=list(df_Dose_Slot["patient"])).values("person", "given_name", "surname","dob", "gender", "race", "ethnicity", "phone", "email", "street", "city", "zip_code", "state", "address_type")
    for dicto in qsPatient:
        dicto['DOB_Day'] = dicto["dob"].strftime("%d")
        dicto['DOB_Month'] = dicto["dob"].strftime("%m")
        dicto['DOB_Year'] = dicto["dob"].strftime("%Y")
    dfPatient = pd.DataFrame(list(qsPatient), columns=["person", "given_name", "surname","DOB_Day", "DOB_Month", "DOB_Year", "gender", "race", "ethnicity", "phone", "email", "street", "city", "zip_code", "state", "address_type"])
    df_Dose_Slot_Patient = pd.merge(df_Dose_Slot, dfPatient, left_on="patient", right_on="person", how="left")
    df_Dose_Slot_Patient.rename(columns={"given_name":"Patient First Name", "surname":"Patient Last Name", "gender":"Administrative Sex", "ethnicity":"Ethnic Group", "street":"Street Address", "city":"City", "state":"State", "zip_code":"Zip Code", "email":"Email Address", "phone":"Phone Number", "address_type":"Patient Address Type", "race":"Race"},inplace=True)
    df_Dose_Slot_Patient.drop(columns='person', inplace=True)

    qsVaccineType = VaccineType.objects.filter(id__in=list(df_Dose_Slot_Patient["vaccineType"])).values("id", "name")
    dfVaccineType = pd.DataFrame(list(qsVaccineType), columns=["id", "name"])

    df_Dose_Slot_Patient_VaccineType = pd.merge(df_Dose_Slot_Patient, dfVaccineType, left_on="vaccineType", right_on="id", how="left")
    df_Dose_Slot_Patient_VaccineType.drop(columns="id", inplace=True)
    df_Dose_Slot_Patient_VaccineType.rename(columns={"name":"Vaccine Manufacturer Name"}, inplace=True)

    df_Dose_Slot_Patient_VaccineType.drop(columns=["slot", "vaccineType"], inplace=True)
    # df_Dose_Slot_Patient_VaccineType = df_Dose_Slot_Patient_VaccineType[["patient", "Site ID", "Booking Start", "Booking End", "Patient Last Name", "DOB_Day", "DOB_Month", "DOB_Year", "Administrative Sex", "Race", "Ethnic Group", "Street Address", "City", "State", "Zip Code", "Patient Address Type", "Phone Number", "Email Address", "Date of Administration", "Vaccine Administered Amount", "Vaccine Lot Number", "Vaccine Manufacturer Name", "Vaccine Route of Administration"]]

    qsAnswers = MedicalEligibilityAnswer.objects.all().values("person", "question", "answer_text")
    dfAnswers = pd.DataFrame(list(qsAnswers), columns=["person", "question", "answer_text"])
    qsQuestions = MedicalEligibilityQuestion.objects.all().values("id", "question")
    dfQuestions = pd.DataFrame(list(qsQuestions), columns=["id", "question"])
    df_Questions_Answers = pd.merge(dfAnswers, dfQuestions, left_on="question", right_on="id", how="left")
    df_Questions_Answers.drop(columns=["question_x", "id"], inplace=True)
    df_Questions_Answers = df_Questions_Answers.pivot(index="person", columns="question_y", values="answer_text")
    # df_Questions_Answers = df_Questions_Answers[["Do you have a bleeding disorder or are you on medication that affects your immune system?", "Do you have any allergies to medication, and/or have you ever had an adverse reaction to a vaccine?", "Do you have a fever?", "Are you pregnant or do you plan to become pregnant soon?", "Are you currently breastfeeding?", "Have you received another COVID-19 vaccine?", "Have you had any OTHER vaccine in the last 14 days?", "Will you be available for your second dose in approximately 4 weeks?", "Comments"]]

    df_final = pd.merge(df_Dose_Slot_Patient_VaccineType, df_Questions_Answers, left_on="patient", right_on="person", how="left")
    df_final.drop(columns="patient", inplace=True)
    df_final = df_final[["Site ID", "Booking Start", "Booking End", "Patient Last Name", "Patient First Name", "DOB_Day", "DOB_Month", "DOB_Year", "Administrative Sex", "Race", "Ethnic Group", "Street Address", "City", "State", "Zip Code", "Patient Address Type", "Phone Number", "Email Address", "Do you have a bleeding disorder or are you on medication that affects your immune system?", "Do you have any allergies to medication, and/or have you ever had an adverse reaction to a vaccine?", "Do you have a fever?", "Are you pregnant or do you plan to become pregnant soon?", "Are you currently breastfeeding?", "Have you received another COVID-19 vaccine?", "Have you had any OTHER vaccine in the last 14 days?", "Will you be available for your second dose in approximately 4 weeks?", "Comments", "Date of Administration", "Vaccine Administered Amount", "Vaccine Lot Number", "Vaccine Manufacturer Name", "Vaccine Route of Administration"]]

    df_final.to_csv(response)
    return response




    # qsPatient = Person.objects.filter(pk__in=list(df_Dose_Slot["patient"])).values("id",  "givenName", "surName","dateOfBirth", "gender", "race", "ethnicity", "phoneNumber", "emailAddress", "street", "city", "zipCode", "state", "addressType")
    # dfPatient = pd.DataFrame(list(qsPatient), columns=["id", "givenName", "surName", "dateOfBirth", "gender", "race", "ethnicity", "phoneNumber", "emailAddress", "street", "city", "zipCode", "state", "addressType"])


    # df_Dose_Slot_Patient = pd.merge(df_Dose_Slot, dfPatient, left_on="id", right_on="id", how="left")
        #
    # qsVaccineBatch = VaccineBatch.objects.filter(id__in=list(df_Dose_Slot_Patient["vaccine"])).values("id", "batch", "site", "vaccineType")
    # dfVaccineBatch = pd.DataFrame(list(qsVaccineBatch), columns = ["id", "batch", "site", "vaccineType"])
        #
    # df_Dose_Slot_Patient_VaccineBatch = pd.merge(df_Dose_Slot_Patient, dfVaccineBatch, left_on="id", right_on="id", how="left")
        #
        #
    # df_Dose_Slot.to_csv(response)
    #
    # return response

#
# def detail(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="csvfile.csv"'
#
#     date_range = [datetime.date(2021, 5, 2), datetime.date(2021, 5, 3)] #replace with input from forms
#
#     qsSlot = Slot.objects.filter(startTime__range = date_range).values("id", "site", "startTime", "duration", 'capacity', "vaccineType")
#     for dicto  in qsSlot:
#         dicto['endTime'] = dicto['startTime'] + datetime.timedelta(minutes=+int(dicto['duration']))
#     dfSlot = pd.DataFrame(list(qsSlot), columns=["id", "site", "startTime", "endTime", "capacity", "vaccineType"])
#
#     qsDose = Dose.objects.filter(slot__in=list(dfSlot["id"])).values("id", "patient", "vaccine", "amount", 'administered', "location", "timeVax", "slot")
#     dfDose = pd.DataFrame(list(qsDose), columns=["id", "patient", "vaccine", "amount_administered", "administered", "timeVax", "slot"])
#
#     df_Dose_Slot = pd.merge(dfSlot, dfDose, left_on="id", right_on="id", how="left")
#
#
#     qsPatient = Person.objects.filter(pk__in=list(df_Dose_Slot["patient"])).values("id",  "givenName", "surName","dateOfBirth", "gender", "race", "ethnicity", "phoneNumber", "emailAddress", "street", "city", "zipCode", "state", "addressType")
#     dfPatient = pd.DataFrame(list(qsPatient), columns=["id", "givenName", "surName", "dateOfBirth", "gender", "race", "ethnicity", "phoneNumber", "emailAddress", "street", "city", "zipCode", "state", "addressType"])
#
#
#     df_Dose_Slot_Patient = pd.merge(df_Dose_Slot, dfPatient, left_on="id", right_on="id", how="left")
#
#     qsVaccineBatch = VaccineBatch.objects.filter(id__in=list(df_Dose_Slot_Patient["vaccine"])).values("id", "batch", "site", "vaccineType")
#     dfVaccineBatch = pd.DataFrame(list(qsVaccineBatch), columns = ["id", "batch", "site", "vaccineType"])
#
#     df_Dose_Slot_Patient_VaccineBatch = pd.merge(df_Dose_Slot_Patient, dfVaccineBatch, left_on="id", right_on="id", how="left")
#
#
#     df_Dose_Slot_Patient_VaccineBatch.to_csv(response)
#
#     return response
