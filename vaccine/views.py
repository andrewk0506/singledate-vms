#from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Personmini, Slot, Person,Dose
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
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'vaccine/detail.html'


class ResultsView(generic.DetailView):
    model = Question
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
    create_dummydata()
    return render(request, 'vaccine/dashboard.html')

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

    # try:
    # print(request.POST['datepicker'])
    will_be_unique = Personmini.objects.all()
    canuarray = [4,5,6]

    activateDates = []
    i = ""
    for i in will_be_unique:
        print(i.datevaccinatednumone)
        #convert to day/month/year
        print(i.datevaccinatednumone.day)
        activateDates.append(makeDateCal(i.datevaccinatednumone))
    print(activateDates)
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
        print(i.startTime)
        #convert to day/month/year
        print(i.startTime.day)
        activateDates.append(makeDateCal(i.startTime))
    print(activateDates)
    defaultDate = makeDefaultDate(i.startTime)



    context = {'canuarray': canuarray,
               'activateDates':activateDates,
               'defaultDate':defaultDate}
    return render(request, 'vaccine/dashboardreal.html',context)


def daterangereal(request):
    try:
        print("TRYING")
        x = datetime.datetime.strptime(request.POST['datepicker'], '%m/%d/%Y')
    except:
        print("CATCH!")
        return render(request, 'vaccine/daterangereal.html', {
            # 'error_message': "Select date",
        })
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
        filteredDate = Slot.objects.filter(startTime__startswith=x).values("id", "site", "startTime", "duration", 'capacity', "vaccineType")
        return filteredDate

    # vaccinated_people = filterData(one, two)
    # print(makeDate(one))
    qsSlot = filterDate(x)
    ## ADD TABLE QUERIES AND MAKE CSV
    print(qsSlot)
    for dicto in qsSlot:
        dicto['endTime'] = dicto['startTime'] + datetime.timedelta(minutes=+int(dicto['duration']))
    dfSlot = pd.DataFrame(list(qsSlot), columns=["id", "site", "startTime", "endTime", "capacity", "vaccineType"])

    qsDose = Dose.objects.filter(slot__in=list(dfSlot["id"])).values("id", "patient", "vaccine", "amount", 'administered', "location", "timeVax", "slot")
    dfDose = pd.DataFrame(list(qsDose), columns=["id", "patient", "vaccine", "amount_administered", "administered", "timeVax", "slot"])

    df_Dose_Slot = pd.merge(dfSlot, dfDose, left_on="id", right_on="id", how="left")


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
    df_Dose_Slot.to_csv(response)

    return response

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