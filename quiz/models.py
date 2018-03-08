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

class Assessment(models.Model):
	name=models.CharField(max_length=250, blank=False)
	date=models.DateTimeField(blank=False)
	max_marks=models.IntegerField(null=False)
	no_of_questions=models.IntegerField(null=False)
	duration=models.IntegerField(null=False)
	description=models.CharField(max_length=2000, blank=True)

	def __str__(self):
		return self.name + " " + str(self.date)



class Question(models.Model):
	assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
	question=models.CharField(max_length=1000)
	option_a=models.CharField(max_length=250)
	option_b=models.CharField(max_length=250)
	option_c=models.CharField(max_length=250)
	option_d=models.CharField(max_length=250)
	solution=models.CharField(max_length=2)

	def __str__(self):
		return self.question

class timeRemaining(models.Model):
	user=models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
	assessment=models.ForeignKey(Assessment,default=None, on_delete=models.CASCADE)
	timeStart=models.DateTimeField(blank=False)
	timeEnd=models.DateTimeField(blank=False)

	def __str__(self):
		return str(self.user)+str(timeStart)+str(timeEnd)