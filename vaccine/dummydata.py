from .models import VaccineBatch, VaccineType, Site, Slot, Staff, Patient, Station, Dose, MedicalEligibilityQuestion, \
    MedicalEligibilityAnswer
import datetime


def create_dummydata():

    num_sites_types = 50
    num_batches = 500
    num_appts = 1000
    sites = []
    vaccine_types = []
    stations = []
    staffs = []
    vaccine_batches = []
    questions = []

    questions_text = ["Do you have a bleeding disorder or are you on medication that affects your immune system?",
                 "Do you have any allergies to medication, and/or have you ever had an adverse reaction to a vaccine?",
                 "Do you have a fever?",
                 "Are you pregnant or do you plan to become pregnant soon?",
                 "Are you currently breastfeeding?",
                 "Have you received another COVID-19 vaccine?",
                 "Have you had any OTHER vaccine in the last 14 days?",
                 "Will you be available for your second dose in approximately 4 weeks?",
                 "Comments"]
    for quest in questions_text:
        q = MedicalEligibilityQuestion(label="label", language="english", question=quest, explanation="cuz")
        questions.append(q)
        q.save()
    for i in range(num_sites_types):

        vaccine_types.append(VaccineType(name='vaccine'+str(i+1), daysUntilNext=5))
        sites.append(Site(street='Sesame', city='Sunny Water', zipCode='12353', comments='woo'))
        vaccine_types[i].save()
        sites[i].save()

        stations.append(Station(site=sites[i], stationName = 'station'+str(i+1)))
        stations[i].save()
        staffs.append(Staff(last_name='laststaff'+str(i+1), first_name = 'firststaff'+str(i+1), phone_number='123678',
                            email='email@emailstaff'+str(i+1), password='whyisthisstoredinplaintext',
                            HIPAACert=datetime.datetime.now(), medical_id=i, role='staff i guess?'))
        staffs[i].save()

    for i in range(num_batches):

        vaccine_batches.append(VaccineBatch(batch=i, site = sites[i % num_sites_types],
                                           vaccineType=vaccine_types[i % num_sites_types]))
        vaccine_batches[i].save()

    for i in range(num_appts):

        chosen_date = datetime.datetime(2021, 5, 2, 12, 30) + datetime.timedelta(hours=+i)

        p = Patient.objects.create(surname='testsur'+str(i+1), given_name='testname'+str(i+1),
                                  dob= datetime.date(1776, 12, 4), phone='12344567',
                                  email= 'email@email.com', street='street', city='city', zip_code='zip')

        p.save()
        for quest in questions:
            m = MedicalEligibilityAnswer(person = p, question = quest, answered = chosen_date,
                                         answer_text = quest.question + " NUMBER: " +str(i+1))
            m.save()
        sl = Slot.objects.create(site=sites[i % num_sites_types], startTime=chosen_date, duration=10, capacity=50,
                                 vaccineType=vaccine_types[i % num_sites_types])
        sl.save()

        d = Dose.objects.create(patient=p, vaccine=vaccine_batches[i % num_batches], amount =0.1, administered='i',
                                location='LD', vaccinator=staffs[i % num_sites_types],
                                station=stations[i % num_sites_types], signIn=chosen_date,
                                timeVax=chosen_date + datetime.timedelta(minutes=+1), slot=sl, secondDose=True)
        d.save()

