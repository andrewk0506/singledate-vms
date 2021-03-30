from django.db import models
from django.core.validators import validate_email
from phone_field import PhoneField

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

class User(models.Model):
    """
    Table of user's personal and contact information.
    """
    ### Define field choices.
    GENDER = [('M', 'Male'),
              ('F', 'Female'),
              ('X', 'Non-binary'),
              ('N', 'null')]
    RACE = [('A', 'American Indian/Alaskan Native'),
            ('S', 'Asian'),
            ('B', 'Black/African American'),
            ('P', 'Native Hawaiian/Other Pacific Islander'),
            ('W', 'White'),
            ('O', 'Other Race'),
            ('X', 'Prefer not to specify')]
    ETHNICITY = [('H', 'Hispanic'),
                 ('N', 'Non-hispanic'),
                 ('X', 'Prefer not to specify')]
    ADDRESS_TYPES = [('H', 'Home'),
                     ('C', 'Current/Temporary'),
                     ('P', 'Permanet'),
                     ('M', 'Mailing')]
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
    
    ### Personal Data
    person = models.AutoField(primary_key=True)
    given_name = models.CharField(max_length=100) # Not null by default.
    surname = models.CharField(max_length=100) # Not null by default.
    dob = models.DateField() # Not null by default.
    gender = models.CharField(max_length=1, choices=GENDER) # Not null by default.
    race = models.CharField(max_length=1, choices=RACE) # Not null by default.
    ethnicity = models.CharField(max_length=1, choices=ETHNICITY) # Not null by default.
    
    ### Contact Info
    phone = PhoneField(blank=True)
    email = models.EmailField(validators=[validate_email]) # Not null by default.
    street = NoCommaField(max_length=100) # Not null by default.
    city = models.CharField(max_length=100) # Not null by default.
    zip_code = models.CharField(max_length=5) # Not null by default.
    state = models.CharField(max_length=2, choices=STATES, default="NJ")
    address_type = models.CharField(max_length=1, choices=ADDRESS_TYPES)
