# Generated by Django 3.1.7 on 2021-04-09 01:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models
import vaccine.models


class Migration(migrations.Migration):

    dependencies = [
        ('vaccine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicalEligibilityQuestion',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=10)),
                ('language', models.CharField(max_length=20)),
                ('question', models.CharField(max_length=255)),
                ('explanation', models.TextField()),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('X', 'Non binary')], default=vaccine.models.Gender['F'], max_length=1)),
                ('bool', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('person', models.AutoField(primary_key=True, serialize=False)),
                ('given_name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male'), ('X', 'Non binary')], default=vaccine.models.Gender['F'], max_length=1)),
                ('race', models.CharField(choices=[('A', 'American Indian/Alaskan Native'), ('S', 'Asian'), ('B', 'Black/African American'), ('P', 'Native Hawaiian/Other Pacific Islander'), ('W', 'White'), ('O', 'Other Race'), ('X', 'Prefer not to specify')], default=vaccine.models.Race['X'], max_length=1)),
                ('ethnicity', models.CharField(choices=[('H', 'Hispanic'), ('N', 'Non-hispanic'), ('X', 'Prefer not to specify')], default=vaccine.models.Ethnicity['X'], max_length=1)),
                ('phone', phone_field.models.PhoneField(blank=True, max_length=31)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('street', vaccine.models.NoCommaField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=5)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default=vaccine.models.States['NJ'], max_length=2)),
                ('address_type', models.CharField(choices=[('H', 'Home'), ('C', 'Current/Temporary'), ('P', 'Permanet'), ('M', 'Mailing')], default=vaccine.models.AddressType['H'], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surName', models.CharField(max_length=100)),
                ('givenName', models.CharField(max_length=100)),
                ('dateOfBirth', models.DateTimeField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('X', 'Non-Binary'), ('O', 'Other/Prefer not to specify')], default='O', max_length=1)),
                ('race', models.CharField(choices=[('A', 'American Indian/Alaskan Native'), ('S', 'Asian'), ('B', 'Black/African American'), ('P', 'Native Hawaiian/Other Pacific Islander'), ('W', 'White'), ('O', 'Other'), ('X', 'Prefer not to specify')], default='X', max_length=1)),
                ('ethnicity', models.CharField(choices=[('H', 'Hispanic'), ('N', 'Not Hispanic'), ('X', 'Prefer not to specify')], default='X', max_length=1)),
                ('phoneNumber', models.CharField(max_length=10)),
                ('emailAddress', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipCode', models.CharField(max_length=5)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='NJ', max_length=2)),
                ('addressType', models.CharField(choices=[('H', 'Home'), ('B', 'Billing'), ('S', 'Business'), ('C', 'Contact')], default='H', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Personmini',
            fields=[
                ('personid', models.AutoField(primary_key=True, serialize=False)),
                ('givenname', models.CharField(blank=True, db_column='GivenName', max_length=100, null=True)),
                ('surname', models.CharField(blank=True, db_column='SurName', max_length=100, null=True)),
                ('dateofbirth', models.DateField(blank=True, db_column='DateOfBirth', null=True)),
                ('datevaccinatednumone', models.DateTimeField(blank=True, db_column='DateVaccinatedNumOne', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zipCode', models.CharField(max_length=5)),
                ('state', models.CharField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')], default='NJ', max_length=2)),
                ('comments', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=40, null=True)),
                ('email', models.CharField(max_length=60)),
                ('password', models.CharField(max_length=60, null=True)),
                ('HIPAACert', models.DateTimeField(blank=True, null=True)),
                ('medical_id', models.IntegerField(blank=True, null=True)),
                ('role', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='VaccineType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('daysUntilNext', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VaccineBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.IntegerField()),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.site')),
                ('vaccineType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.vaccinetype')),
            ],
        ),
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stationName', models.CharField(max_length=50)),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.site')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('startTime', models.DateTimeField()),
                ('duration', models.SmallIntegerField(verbose_name=3)),
                ('capacity', models.IntegerField()),
                ('site', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.site')),
                ('vaccineType', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.vaccinetype')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalEligibilityAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answered', models.DateTimeField()),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.patient')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.medicaleligibilityquestion')),
            ],
        ),
        migrations.CreateModel(
            name='MedicalEligibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('S', 'Screening'), ('E', 'Eligibility')], max_length=1)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.medicaleligibilityquestion')),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('ipAddress', models.CharField(max_length=40)),
                ('webRequest', models.CharField(max_length=64)),
                ('tableName', models.CharField(max_length=100)),
                ('alteredObject', models.TextField(blank=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.staff')),
            ],
        ),
        migrations.CreateModel(
            name='Dose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('administered', models.CharField(max_length=2)),
                ('location', models.CharField(choices=[('LUA', 'Left Upper Arm'), ('LD', 'Left Deltoid'), ('LGM', 'Left Gluteous Medius'), ('LLF', 'Left Lower Forearm'), ('LT', 'Left Thigh'), ('LVL', 'Left Vastus Lateralis'), ('RUA', 'Right Upper Arm'), ('RD', 'Right Deltoid'), ('RGM', 'Right Gluteous Medius'), ('RLF', 'Right Lower Forearm'), ('RT', 'Right Thigh'), ('RVL', 'Right Vastus Lateralis')], max_length=3)),
                ('signIn', models.DateTimeField()),
                ('timeVax', models.DateTimeField()),
                ('secondDose', models.BooleanField()),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.person')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vaccine.slot')),
                ('station', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.station')),
                ('vaccinator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.staff')),
                ('vaccine', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='vaccine.vaccinebatch')),
            ],
        ),
    ]
