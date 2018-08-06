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
	live=models.BooleanField(default=False)
	conformation_mail=	models.IntegerField(null=False, default=0)
	accecpted_requests = models.ManyToManyField(User,related_name='accecpted_requests')
	pending_requests = models.ManyToManyField(User,related_name='pending_requests')
	def __str__(self):
		return self.name + " " + str(self.date)



class Question(models.Model):
	assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
	question=models.CharField(max_length=1000)
	option_a=models.CharField(max_length=250)
	option_b=models.CharField(max_length=250)
	option_c=models.CharField(max_length=250,blank=True)
	option_d=models.CharField(max_length=250,blank=True)
	option_e=models.CharField(max_length=250,blank=True)
	option_f=models.CharField(max_length=250,blank=True)
	option_g=models.CharField(max_length=250,blank=True)
	option_h=models.CharField(max_length=250,blank=True)
	question_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_a_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_b_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_c_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_d_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_e_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_f_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_g_image=models.ImageField(upload_to='media',null=True, blank=True)
	option_h_image=models.ImageField(upload_to='media',null=True, blank=True)
	# question_image=models.CharField(default=None, max_length=250,blank=True, null=True)
	# option_a_image=models.CharField(default=None, max_length=250,blank=True, null=True)
	# option_b_image=models.CharField(default=None, max_length=250,blank=True, null=True)
	# option_c_image=models.CharField(default=None, max_length=250,blank=True, null=True)
	# option_d_image=models.CharField(default=None, max_length=250,blank=True, null=True)
	solution=models.CharField(max_length=2)

	def __str__(self):
		return self.question.encode('utf-8')

class Random_questions(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
	random_ques = models.ManyToManyField(Question)

class timeRemaining(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
	timeStart=models.DateTimeField(blank=False)
	timeEnd=models.DateTimeField(blank=False)
	questions=models.ManyToManyField(Question)

	def __str__(self):
		return str(self.user)+str(self.timeStart)+str(self.timeEnd)

class Response(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE)
	assessment=models.ForeignKey(Assessment, on_delete=models.CASCADE)
	question=models.ForeignKey(Question, on_delete=models.CASCADE)
	response=models.CharField(max_length=2)

	def __str__(self):
		return str(self.user) + str(self.assessment.pk) + str(self.question.pk)
 
