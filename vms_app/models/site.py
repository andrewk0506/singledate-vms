from django.db import models

class Site(models.Model):
	
	class Meta:
		app_label = "vms_app"

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
		choices = STATES,
		default = "NJ",
	)
	comments = models.TextField()