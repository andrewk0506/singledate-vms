from django.db import models

class Person(models.Model):

	class Meta:
		app_label = "vms_app"
	
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
	gender = models.CharField(max_length=1, choices = GENDERS, default="O")
	race = models.CharField(max_length=1, choices = RACES, default = "X")
	ethnicity = models.CharField(max_length=1, choices = ETHNICITIES, default = "X")
	phoneNumber = models.CharField(max_length=10)
	emailAddress = models.CharField(max_length=100)
	street = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	zipCode = models.CharField(max_length=5)
	state = models.CharField(max_length=2, choices = STATES, default = "NJ",)
	addressType = models.CharField(max_length=1, choices = ADDRESS_TYPES, default = "H")
