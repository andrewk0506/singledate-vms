#from django.shortcuts import render

# Create your views here.
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render

from django.urls import reverse
from django.views import generic

from .models import Choice, Question, Personmini
from djqscsv import write_csv
from djqscsv import render_to_csv_response


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


def daterange(request):
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

    def makeDate(datetimeobj):
        x = str(datetimeobj.year) + '-'
        if(len(str(datetimeobj.month))==1):
            x = x + '0' + str(datetimeobj.month) + '-'
        else:
            x = x + str(datetimeobj.month) + '-'
        if(len(str(datetimeobj.day))==1):
            x = x + '0' + str(datetimeobj.day)
        else:
            x = x + str(datetimeobj.day)
        return x

    # vaccinated_people = filterData(one, two)
    # print(makeDate(one))
    vaccinated_people = filterDate(one)
    ## ADD TABLE QUERIES AND MAKE CSV
    print(vaccinated_people)
    context = {'vaccinated_people': vaccinated_people}
    with open('vaccinated_date_range.csv', 'wb') as csv_file:
        write_csv(vaccinated_people, csv_file)
    return render_to_csv_response(vaccinated_people)
    # return render(request, 'vaccine/dateRange.html', context)

def dashboard(request):
    # print(request.POST['datepicker'])
    # print(request.POST['datepicker2'])
    latest_question_list = Question.objects.order_by('-pub_date')[:3]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'vaccine/dashboard.html', context)

def dashboard2(request):
    # activateDates = []
    # for i in Personmini.objects.all():
    #     activateDates.append(i.datevaccinatednumone)
    # print(activateDates)
    activateDates = Personmini.objects.all()
    context = {'activateDates':activateDates}
    try:
        print(request.POST['datepicker'])
        # print(request.POST['datepicker2'])
    except (KeyError):
    # # Redisplay the question voting form.
    #     return render(request, 'vaccine/detail.html', {
    #         'question': question,
    #         'error_message': "You didn't select a choice.",
    #     })
        print("no selection yet")
    return render(request, 'vaccine/dashboard2.html')