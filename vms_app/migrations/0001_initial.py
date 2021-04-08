import django.core.validators
from django.db import migrations, models
import django.db.models.deletion

# import phone_field.models
import vms_app.models.user
import vms_app.models.utils

# Generated by Django 3.1.7 on 2021-04-06 02:50


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MedicalEligibilityQuestion",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("label", models.CharField(max_length=10)),
                ("language", models.CharField(max_length=20)),
                ("question", models.CharField(max_length=255)),
                ("explanation", models.TextField()),
                (
                    "gender",
                    models.CharField(
                        choices=[("F", "Female"), ("M", "Male"), ("X", "Non binary")],
                        default=vms_app.models.utils.Gender["F"],
                        max_length=1,
                    ),
                ),
                ("bool", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="Patient",
            fields=[
                ("person", models.AutoField(primary_key=True, serialize=False)),
                ("given_name", models.CharField(max_length=100)),
                ("surname", models.CharField(max_length=100)),
                ("dob", models.DateField()),
                (
                    "gender",
                    models.CharField(
                        choices=[
                            ("M", "Male"),
                            ("F", "Female"),
                            ("X", "Non-binary"),
                            ("N", "null"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "race",
                    models.CharField(
                        choices=[
                            ("A", "American Indian/Alaskan Native"),
                            ("S", "Asian"),
                            ("B", "Black/African American"),
                            ("P", "Native Hawaiian/Other Pacific Islander"),
                            ("W", "White"),
                            ("O", "Other Race"),
                            ("X", "Prefer not to specify"),
                        ],
                        max_length=1,
                    ),
                ),
                (
                    "ethnicity",
                    models.CharField(
                        choices=[
                            ("H", "Hispanic"),
                            ("N", "Non-hispanic"),
                            ("X", "Prefer not to specify"),
                        ],
                        max_length=1,
                    ),
                ),
                #commented out since throwing error -- ask auth team about this
                #("phone", phone_field.models.PhoneField(blank=True, max_length=31)),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        validators=[django.core.validators.EmailValidator()],
                    ),
                ),
                ("street", vms_app.models.user.NoCommaField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("zip_code", models.CharField(max_length=5)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("AL", "Alabama"),
                            ("AK", "Alaska"),
                            ("AS", "American Samoa"),
                            ("AZ", "Arizona"),
                            ("AR", "Arkansas"),
                            ("CA", "California"),
                            ("CO", "Colorado"),
                            ("CT", "Connecticut"),
                            ("DE", "Delaware"),
                            ("DC", "District of Columbia"),
                            ("FL", "Florida"),
                            ("GA", "Georgia"),
                            ("GU", "Guam"),
                            ("HI", "Hawaii"),
                            ("ID", "Idaho"),
                            ("IL", "Illinois"),
                            ("IN", "Indiana"),
                            ("IA", "Iowa"),
                            ("KS", "Kansas"),
                            ("KY", "Kentucky"),
                            ("LA", "Louisiana"),
                            ("ME", "Maine"),
                            ("MD", "Maryland"),
                            ("MA", "Massachusetts"),
                            ("MI", "Michigan"),
                            ("MN", "Minnesota"),
                            ("MS", "Mississippi"),
                            ("MO", "Missouri"),
                            ("MT", "Montana"),
                            ("NE", "Nebraska"),
                            ("NV", "Nevada"),
                            ("NH", "New Hampshire"),
                            ("NJ", "New Jersey"),
                            ("NM", "New Mexico"),
                            ("NY", "New York"),
                            ("NC", "North Carolina"),
                            ("ND", "North Dakota"),
                            ("MP", "Northern Mariana Islands"),
                            ("OH", "Ohio"),
                            ("OK", "Oklahoma"),
                            ("OR", "Oregon"),
                            ("PA", "Pennsylvania"),
                            ("PR", "Puerto Rico"),
                            ("RI", "Rhode Island"),
                            ("SC", "South Carolina"),
                            ("SD", "South Dakota"),
                            ("TN", "Tennessee"),
                            ("TX", "Texas"),
                            ("UT", "Utah"),
                            ("VT", "Vermont"),
                            ("VI", "Virgin Islands"),
                            ("VA", "Virginia"),
                            ("WA", "Washington"),
                            ("WV", "West Virginia"),
                            ("WI", "Wisconsin"),
                            ("WY", "Wyoming"),
                        ],
                        default="NJ",
                        max_length=2,
                    ),
                ),
                (
                    "address_type",
                    models.CharField(
                        choices=[
                            ("H", "Home"),
                            ("C", "Current/Temporary"),
                            ("P", "Permanet"),
                            ("M", "Mailing"),
                        ],
                        max_length=1,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicalEligibilityAnswer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("answered", models.DateTimeField()),
                (
                    "person",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vms_app.patient",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vms_app.medicaleligibilityquestion",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="MedicalEligibility",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("S", "Screening"), ("E", "Eligibility")], max_length=1
                    ),
                ),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vms_app.medicaleligibilityquestion",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Role",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("role", models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name="Site",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("street", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("zipCode", models.CharField(max_length=5)),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("AL", "Alabama"),
                            ("AK", "Alaska"),
                            ("AS", "American Samoa"),
                            ("AZ", "Arizona"),
                            ("AR", "Arkansas"),
                            ("CA", "California"),
                            ("CO", "Colorado"),
                            ("CT", "Connecticut"),
                            ("DE", "Delaware"),
                            ("DC", "District of Columbia"),
                            ("FL", "Florida"),
                            ("GA", "Georgia"),
                            ("GU", "Guam"),
                            ("HI", "Hawaii"),
                            ("ID", "Idaho"),
                            ("IL", "Illinois"),
                            ("IN", "Indiana"),
                            ("IA", "Iowa"),
                            ("KS", "Kansas"),
                            ("KY", "Kentucky"),
                            ("LA", "Louisiana"),
                            ("ME", "Maine"),
                            ("MD", "Maryland"),
                            ("MA", "Massachusetts"),
                            ("MI", "Michigan"),
                            ("MN", "Minnesota"),
                            ("MS", "Mississippi"),
                            ("MO", "Missouri"),
                            ("MT", "Montana"),
                            ("NE", "Nebraska"),
                            ("NV", "Nevada"),
                            ("NH", "New Hampshire"),
                            ("NJ", "New Jersey"),
                            ("NM", "New Mexico"),
                            ("NY", "New York"),
                            ("NC", "North Carolina"),
                            ("ND", "North Dakota"),
                            ("MP", "Northern Mariana Islands"),
                            ("OH", "Ohio"),
                            ("OK", "Oklahoma"),
                            ("OR", "Oregon"),
                            ("PA", "Pennsylvania"),
                            ("PR", "Puerto Rico"),
                            ("RI", "Rhode Island"),
                            ("SC", "South Carolina"),
                            ("SD", "South Dakota"),
                            ("TN", "Tennessee"),
                            ("TX", "Texas"),
                            ("UT", "Utah"),
                            ("VT", "Vermont"),
                            ("VI", "Virgin Islands"),
                            ("VA", "Virginia"),
                            ("WA", "Washington"),
                            ("WV", "West Virginia"),
                            ("WI", "Wisconsin"),
                            ("WY", "Wyoming"),
                        ],
                        default="NJ",
                        max_length=2,
                    ),
                ),
                ("comments", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="VaccineType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("daysUntilNext", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="VaccineBatch",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("batch", models.IntegerField()),
                (
                    "site",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.site",
                    ),
                ),
                (
                    "vaccineType",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.vaccinetype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Station",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stationName", models.CharField(max_length=50)),
                (
                    "site",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.site",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("surName", models.CharField(max_length=100)),
                ("givenName", models.CharField(max_length=100)),
                ("phoneNumber", models.CharField(max_length=40)),
                ("email", models.CharField(max_length=60)),
                ("medicalId", models.DecimalField(decimal_places=0, max_digits=10)),
                ("HIPAACert", models.DateTimeField()),
                ("password", models.CharField(max_length=60)),
                (
                    "role",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.role",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Slot",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("startTime", models.DateTimeField()),
                ("duration", models.SmallIntegerField(verbose_name=3)),
                ("capacity", models.IntegerField()),
                (
                    "site",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.site",
                    ),
                ),
                (
                    "vaccineType",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.vaccinetype",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Dose",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("amount", models.FloatField()),
                ("administered", models.CharField(max_length=2)),
                (
                    "location",
                    models.CharField(
                        choices=[
                            ("LUA", "Left Upper Arm"),
                            ("LD", "Left Deltoid"),
                            ("LGM", "Left Gluteous Medius"),
                            ("LLF", "Left Lower Forearm"),
                            ("LT", "Left Thigh"),
                            ("LVL", "Left Vastus Lateralis"),
                            ("RUA", "Right Upper Arm"),
                            ("RD", "Right Deltoid"),
                            ("RGM", "Right Gluteous Medius"),
                            ("RLF", "Right Lower Forearm"),
                            ("RT", "Right Thigh"),
                            ("RVL", "Right Vastus Lateralis"),
                        ],
                        max_length=3,
                    ),
                ),
                ("signIn", models.DateTimeField()),
                ("timeVax", models.DateTimeField()),
                ("secondDose", models.BooleanField()),
                (
                    "patient",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.patient",
                    ),
                ),
                (
                    "slot",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vms_app.slot"
                    ),
                ),
                (
                    "station",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.station",
                    ),
                ),
                (
                    "vaccinator",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.staff",
                    ),
                ),
                (
                    "vaccine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="vms_app.vaccinebatch",
                    ),
                ),
            ],
        ),
    ]
