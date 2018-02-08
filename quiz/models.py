from django.db import models
from django.contrib.auth.models import User



class registerRequests(models.Model):
	first_name = models.CharField(max_length=250, blank=False)
	last_name = models.CharField(max_length=250, blank=False)

	# TODO: Check in IIIT-Delhi Email ID
	e_mail = models.CharField(max_length=250, blank=False)

	#todo: try hashing the password field: security 101 password saved as clear text
	password=models.CharField(max_length=250, blank=False)

	#todo: remove confirm password because it is redundant
	confirm_password=models.CharField(max_length=250, blank=False)

	def __str__(self):
		return self.first_name + " " + self.last_name
