from vms_app.models import VaccineBatch, VaccineType, Site, Slot, Staff, Patient, Station, Dose, MedicalEligibilityQuestion, \
    MedicalEligibilityAnswer, Role
from django.contrib.auth.models import User

from allauth.account.models import EmailAddress
from datetime import datetime, timezone, timedelta, date
import random

def create_data():
    days = [datetime(2021, 5, 2, 8, 30, tzinfo=timezone.utc) + timedelta(minutes=+(30* i)) for i in range(16)] +\
           [datetime(2021, 5, 3, 8, 30, tzinfo=timezone.utc) + timedelta(minutes=+(30* i)) for i in range(16)]
    num_sites_types = 5
    num_batches = 50
    sites = []
    vaccine_types = []
    stations = {}
    staffs = []
    vaccine_batches = []
    questions = []
    slots = []
    adminstaffs = []

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
    for i in range(3):
        vaccine_types.append(VaccineType(name='vaccine' + str(i + 1), daysUntilNext=5, amount=0.1))
        vaccine_types[i].save()
    stationcount = 0
    patientcount = 0
    for i in range(num_sites_types):

        sites.append(Site(street='Site Street ' + str(i), city='Site City ' + str(i), zipCode='12353', comments='woo'))
        sites[i].save()


        # staffuser = User.objects.create_user(username='user'+str(i+1), email='admin'+ str(i+1) + '@emailstaff.com', password='password')
        # staffuser.save()
        # adminrole = Role(role = "A", site=sites[i])
        # adminrole.save()
        # adminstaffs.append(Staff(user = staffuser, last_name='adminstaff'+str(i+1), first_name = 'adminstaff'+str(i+1), phone_number='123678',
        #                     email='admin'+ str(i+1) + '@emailstaff.com',
        #                     HIPAACert=datetime.now(), medical_id=i, role=adminrole))
        #
        # adminstaffs[i].save()

        vaccrole = Role(role="V", site=sites[i])
        vaccrole.save()

        for k in range(num_batches):
            vaccine_batches.append(VaccineBatch(batch=i, site=sites[i],
                                                vaccineType=vaccine_types[k % 3]))
            vaccine_batches[i].save()
        stations[i] = []
        x = random.randint(3,10)
        for j in range(x):
            stationcount+=1
            stations[i].append(Station.objects.create(site=sites[i], stationName = 'station'+str(stationcount)))
            stations[i][j].save()
            staff = Staff(last_name='laststaff'+str(stationcount), first_name = 'firststaff'+str(stationcount), phone_number='123678',
                            email='email@emailstaff'+str(i+1),
                            HIPAACert=datetime.now(), medical_id=i, role=vaccrole)
            staff.save()
        for time in days:

            slots.append(Slot.objects.create(site = sites[i], startTime = time, duration = 10, capacity = x, vaccineType = vaccine_types[i%3]))

            slots[-1].save()

            for appt in range(x):
                luck = random.randint(0,10)
                if luck > 3:
                    patientcount += 1
                    p = Patient.objects.create(last_name='testsur' + str(patientcount), first_name='testname' + str(patientcount), middle_initial = "i",
                                               dob=date(1776, 12, 4), phone='12344567',
                                               email='email@email.com', street='street', city='city', zip_code='zip')

                    p.save()
                    for quest in questions:
                        m = MedicalEligibilityAnswer(patient=p, question=quest, answered=time,
                                                     answer_text=quest.question + " NUMBER: " + str(patientcount))
                        m.save()
                    d = Dose.objects.create(patient=p, vaccine=vaccine_batches[i % num_batches],
                                            administered='i',
                                            location='LD', vaccinator=staff,
                                            station=stations[i][appt], signIn=time,
                                            timeVax=time + timedelta(minutes=+1), slot=slots[-1], secondDose=True)
                    d.save()

def create2():
    staffuser = User.objects.create_user(username='sachiyuan', email='SachiYuan@gmail.com',
                                         password='password')
    staffuser.save()
    site = Site.objects.filter(id=1)[0]
    adminrole = Role(role="A", site=site)
    adminrole.save()
    Staff(user=staffuser, last_name='Yuan', first_name='Sachi',
                             phone_number='123678',
                             email='SachiYuan@gmail.com',
                             HIPAACert=datetime.now(), medical_id=120, role=adminrole).save()
    # staffuser._meta.get_field('email').verified = True
    # admin = User.objects.filter(id=1)[0]
    # admin.email
    # EmailAddress.objects.get_or_create(user=admin, email = admin.email, verified = True, primary = True)
