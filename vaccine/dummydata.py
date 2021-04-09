from .models import VaccineBatch, VaccineType, Site, Slot, Staff, Person, Station, Dose
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
    for i in range(num_sites_types):

        vaccine_types.append(VaccineType(name='vaccine'+str(i), daysUntilNext=5))
        sites.append(Site(street='Sesame', city='Sunny Water', zipCode='12353', comments='woo'))
        vaccine_types[i].save()
        sites[i].save()

        stations.append(Station(site=sites[i], stationName = 'station'+str(i)))
        stations[i].save()
        staffs.append(Staff(last_name='laststaff'+str(i), first_name = 'firststaff'+str(i), phone_number='123678',
                            email='email@emailstaff'+str(i), password='whyisthisstoredinplaintext',
                            HIPAACert=datetime.datetime.now(), medical_id=i, role='staff i guess?'))
        staffs[i].save()

    for i in range(num_batches):

        vaccine_batches.append(VaccineBatch(batch=i, site = sites[i % num_sites_types],
                                           vaccineType=vaccine_types[i % num_sites_types]))
        vaccine_batches[i].save()

    for i in range(num_appts):

        chosen_date = datetime.datetime(2021, 5, 2, 12, 30) + datetime.timedelta(hours=+i)

        p = Person.objects.create(surName='testsur'+str(i), givenName='testname'+str(i),
                                  dateOfBirth= datetime.date(1776, 12, 4), phoneNumber='12344567',
                                  emailAddress= 'email@email.com', street='street', city='city', zipCode='zip')
        p.save()
        sl = Slot.objects.create(site=sites[i % num_sites_types], startTime=chosen_date, duration=10, capacity=50,
                                 vaccineType=vaccine_types[i % num_sites_types])
        sl.save()

        d = Dose.objects.create(patient=p, vaccine=vaccine_batches[i % num_batches], amount =0.1, administered='i',
                                location='LD', vaccinator=staffs[i % num_sites_types],
                                station=stations[i % num_sites_types], signIn=chosen_date,
                                timeVax=chosen_date + datetime.timedelta(minutes=+1), slot=sl, secondDose=True)
        d.save()
