# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Personmini(models.Model):
    personid = models.AutoField(primary_key=True)
    givenname = models.CharField(db_column='GivenName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(db_column='SurName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    datevaccinatednumone = models.DateTimeField(db_column='DateVaccinatedNumOne', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PersonMini'

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Personmini(models.Model):
    personid = models.AutoField(primary_key=True)
    givenname = models.CharField(db_column='GivenName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(db_column='SurName', max_length=100, blank=True, null=True)  # Field name made lowercase.
    dateofbirth = models.DateField(db_column='DateOfBirth', blank=True, null=True)  # Field name made lowercase.
    datevaccinatednumone = models.DateTimeField(db_column='DateVaccinatedNumOne', blank=True, null=True)  # Field name made lowercase.


class Site(models.Model):
    STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'),
              ('AR', 'Arkansas'), ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
              ('DE', 'Delaware'), ('DC', 'District of Columbia'), ('FL', 'Florida'),
              ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
              ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
              ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
              ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
              ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'),
              ('NV', 'Nevada'), ('NH', 'New Hampshire'), ('NJ', 'New Jersey'),
              ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
              ('ND', 'North Dakota'), ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'),
              ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('PR', 'Puerto Rico'),
              ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
              ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
              ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'),
              ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=5)
    state = models.CharField(
        max_length=2,
        choices=STATES,
        default="NJ",
    )
    comments = models.TextField()


class VaccineType(models.Model):
    name = models.CharField(max_length=100)
    daysUntilNext = models.IntegerField()


class VaccineBatch(models.Model):
    batch = models.IntegerField()
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL, null=True)


class Slot(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    startTime = models.DateTimeField()
    duration = models.SmallIntegerField(3)
    capacity = models.IntegerField()
    vaccineType = models.ForeignKey(VaccineType, on_delete=models.SET_NULL, null=True)


class Station(models.Model):
    site = models.ForeignKey(Site, on_delete=models.SET_NULL, null=True)
    stationName = models.CharField(max_length=50)


class NoCommaField(models.CharField):
    """
    Helper CharField but with commas replaced by spaces.
    """

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs['max_length']
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        att = getattr(model_instance, self.attname)
        return att.replace(',', ' ')


class Person(models.Model):
    GENDERS = [('M', 'Male'),
               ('F', 'Female'),
               ('X', 'Non-Binary'),
               ('O', 'Other/Prefer not to specify')]

    RACES = [('A', 'American Indian/Alaskan Native'),
             ('S', 'Asian'),
             ('B', 'Black/African American'),
             ('P', 'Native Hawaiian/Other Pacific Islander'),
             ('W', 'White'), ('O', 'Other'),
             ('X', 'Prefer not to specify')]

    ETHNICITIES = [('H', 'Hispanic'),
                   ('N', 'Not Hispanic'),
                   ('X', 'Prefer not to specify')]

    STATES = [('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'),
              ('AZ', 'Arizona'), ('AR', 'Arkansas'), ('CA', 'California'),
              ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
              ('DC', 'District of Columbia'), ('FL', 'Florida'), ('GA', 'Georgia'),
              ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
              ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
              ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
              ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'),
              ('MS', 'Mississippi'), ('MO', 'Missouri'), ('MT', 'Montana'),
              ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
              ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
              ('NC', 'North Carolina'), ('ND', 'North Dakota'),
              ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'),
              ('OK', 'Oklahoma'), ('OR', 'Oregon'), ('PA', 'Pennsylvania'),
              ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'),
              ('SC', 'South Carolina'), ('SD', 'South Dakota'), ('TN', 'Tennessee'),
              ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'),
              ('VI', 'Virgin Islands'), ('VA', 'Virginia'), ('WA', 'Washington'),
              ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')]

    ADDRESS_TYPES = [('H', 'Home'),
                     ('B', 'Billing'),
                     ('S', 'Business'),
                     ('C', 'Contact')]

    surName = models.CharField(max_length=100)
    givenName = models.CharField(max_length=100)
    dateOfBirth = models.DateTimeField()
    gender = models.CharField(max_length=1, choices=GENDERS, default="O")
    race = models.CharField(max_length=1, choices=RACES, default="X")
    ethnicity = models.CharField(max_length=1, choices=ETHNICITIES, default="X")
    phoneNumber = models.CharField(max_length=10)
    emailAddress = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=5)
    state = models.CharField(max_length=2, choices=STATES, default="NJ", )
    addressType = models.CharField(max_length=1, choices=ADDRESS_TYPES, default="H")


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


class Gender(ChoiceEnum):
    F = 'Female'
    M = 'Male'
    X = 'Non binary'


class Race(ChoiceEnum):
    A = 'American Indian/Alaskan Native'
    S = 'Asian'
    B = 'Black/African American'
    P = 'Native Hawaiian/Other Pacific Islander'
    W = 'White'
    O = 'Other Race'
    X = 'Prefer not to specify'


class Ethnicity(ChoiceEnum):
    H = 'Hispanic'
    N = 'Non-hispanic'
    X = 'Prefer not to specify'


class AddressType(ChoiceEnum):
    H = 'Home'
    C = 'Current/Temporary'
    P = 'Permanet'
    M = 'Mailing'


class States(ChoiceEnum):
    AL = 'Alabama'
    AK = 'Alaska'
    AS = 'American Samoa'
    AZ = 'Arizona'
    AR = 'Arkansas'
    CA = 'California'
    CO = 'Colorado'
    CT = 'Connecticut'
    DE = 'Delaware'
    DC = 'District of Columbia'
    FL = 'Florida'
    GA = 'Georgia'
    GU = 'Guam'
    HI = 'Hawaii'
    ID = 'Idaho'
    IL = 'Illinois'
    IN = 'Indiana'
    IA = 'Iowa'
    KS = 'Kansas'
    KY = 'Kentucky'
    LA = 'Louisiana'
    ME = 'Maine'
    MD = 'Maryland'
    MA = 'Massachusetts'
    MI = 'Michigan'
    MN = 'Minnesota'
    MS = 'Mississippi'
    MO = 'Missouri'
    MT = 'Montana'
    NE = 'Nebraska'
    NV = 'Nevada'
    NH = 'New Hampshire'
    NJ = 'New Jersey'
    NM = 'New Mexico'
    NY = 'New York'
    NC = 'North Carolina'
    ND = 'North Dakota'
    MP = 'Northern Mariana Islands'
    OH = 'Ohio'
    OK = 'Oklahoma'
    OR = 'Oregon'
    PA = 'Pennsylvania'
    PR = 'Puerto Rico'
    RI = 'Rhode Island'
    SC = 'South Carolina'
    SD = 'South Dakota'
    TN = 'Tennessee'
    TX = 'Texas'
    UT = 'Utah'
    VT = 'Vermont'
    VI = 'Virgin Islands'
    VA = 'Virginia'
    WA = 'Washington'
    WV = 'West Virginia'
    WI = 'Wisconsin'
    WY = 'Wyoming'


class MedicalEligibilityQuestion(models.Model):
    """
        Medical Eligibility Question schema
    """

    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=10)
    language = models.CharField(max_length=20)
    question = models.CharField(max_length=255)
    explanation = models.TextField()
    gender = models.CharField(max_length=1, choices=Gender.choices(), default=Gender.F)
    bool = models.BooleanField(default=True)


class Patient(models.Model):
    """
    Table of patient's personal and contact information.
    """
    ### Personal Data
    person = models.AutoField(primary_key=True)
    given_name = models.CharField(max_length=100)  # Not null by default.
    surname = models.CharField(max_length=100)  # Not null by default.
    dob = models.DateField()  # Not null by default.
    gender = models.CharField(max_length=1, choices=Gender.choices(), default=Gender.F)
    race = models.CharField(max_length=1, choices=Race.choices(), default=Race.X)
    ethnicity = models.CharField(max_length=1, choices=Ethnicity.choices(), default=Ethnicity.X)

    ### Contact Info
    phone = PhoneField(blank=True)
    email = models.EmailField(validators=[validate_email])  # Not null by default.
    street = NoCommaField(max_length=100)  # Not null by default.
    city = models.CharField(max_length=100)  # Not null by default.
    zip_code = models.CharField(max_length=5)  # Not null by default.
    state = models.CharField(max_length=2, choices=States.choices(), default=States.NJ)
    address_type = models.CharField(max_length=1, choices=AddressType.choices(),
                                    default=AddressType.H)


class MedicalEligibilityAnswer(models.Model):
    """
        Medical Eligibility Answer
    """
    person = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    answered = models.DateTimeField()
    answer = "mediumtext or bool"


class MedicalEligibility(models.Model):
    """
    """
    QUESTION_TYPE = [('S', 'Screening'), ('E', 'Eligibility')]

    # site = models.ForeignKey(Site)
    question = models.ForeignKey(MedicalEligibilityQuestion, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=QUESTION_TYPE)
    start_date = models.DateField()
    end_date = models.DateField()


class Role(models.Model):
    role = models.CharField(max_length=15)


class Staff(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=40, null=True)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=60, null=True)
    HIPAACert = models.DateTimeField(null=True, blank=True)
    medical_id = models.IntegerField(null=True, blank=True)
    role = models.CharField(max_length=60)


class Log(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    ipAddress = models.CharField(max_length=40)
    webRequest = models.CharField(max_length=64)
    tableName = models.CharField(max_length=100)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    alteredObject = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp} {self.ipAddress}"


class Dose(models.Model):
    LOCATIONS = [("LUA", "Left Upper Arm"),
                 ("LD", "Left Deltoid"),
                 ("LGM", "Left Gluteous Medius"),
                 ("LLF", "Left Lower Forearm"),
                 ("LT", "Left Thigh"),
                 ('LVL', "Left Vastus Lateralis"),
                 ('RUA', "Right Upper Arm"),
                 ('RD', "Right Deltoid"),
                 ('RGM', "Right Gluteous Medius"),
                 ('RLF', "Right Lower Forearm"),
                 ('RT', "Right Thigh"),
                 ('RVL', "Right Vastus Lateralis")]

    patient = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True)  # should become foreign key
    vaccine = models.ForeignKey(VaccineBatch, on_delete=models.SET_NULL, null=True)
    amount = models.FloatField()
    administered = models.CharField(max_length=2)
    location = models.CharField(max_length=3, choices=LOCATIONS)
    vaccinator = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True)
    station = models.ForeignKey(Station, on_delete=models.SET_NULL, null=True)
    signIn = models.DateTimeField()
    timeVax = models.DateTimeField()
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    secondDose = models.BooleanField()

