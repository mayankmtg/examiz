from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
import datetime
from django.utils import timezone
from .utils import emailSend, saveFile
import xlsxwriter, zipfile, os, shutil, random, urllib, xlrd
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
	context={}
	return render(request, 'quiz/home.html', context)


def type_login(request):
	if(request.user.is_staff or request.user.is_superuser):
		return redirect('quiz:admin_home')
	else:
		return redirect('quiz:user_home')

def register(request):
	context={}
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		e_mail=request.POST['email']
		print(unicode(e_mail))
		print(User.objects.values_list('email'))
		for m in User.objects.values_list('email'):
			if unicode(e_mail)==m[0]:
				return render(request,'quiz/announcement.html', context={'message':"E-mail Address already exists."})
		print()
		password=request.POST['password']
		confirm_password=request.POST['confirm_password']
		if(password==confirm_password):
			my_uname=e_mail
			my_uname_array=my_uname.split('@')
			userName=my_uname_array[0]
			new_user=User.objects.create_user(userName,first_name=first_name, last_name=last_name, password=password, email=e_mail)
			email_message="Your Account has been created:\nUsername = "+userName
			emailSend("IIITD-Online Quiz 	Account Activation",e_mail,email_message)
			new_user.save()
			return render(request, 'quiz/announcement.html', context={'message':"User Created: Check your Email"})
		else:
			return render(request, 'quiz/announcement.html', context={'message':"Password Mismatch"})
	return render(request, 'quiz/register.html', context)


# Create User views here.

@login_required(login_url='/login')
def user_home(request):
	context={
	}
	return render(request, 'quiz/user_home.html', context)

@login_required(login_url='/login')
def apply_assessments(request):
	context={
		'all_assessments':Assessment.objects.filter(live=True),
	}
	return render(request, 'quiz/apply_assessments.html', context)

@login_required(login_url='/login')
def apply_request(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	user=request.user
	if assessment.pending_requests.filter(email=user.email).count()==0 and assessment.accecpted_requests.filter(email=user.email).count()==0:
		assessment.pending_requests.add(user)
		context={
			'message':'Request Registered',
		}
	elif assessment.pending_requests.filter(email=user.email).count()!=0:
		context={
		'message':'Request already Registered',
		}
	else:
		context={
		'message':'Request accecpted. You can now go to approved exams page.',
		}
	return render(request, 'quiz/announcement.html', context)

@login_required(login_url='/login')
def all_assessments(request):
	user=request.user
	all_assessments=Assessment.objects.filter(live=True)
	assessment_allowed=[]
	for assessment in all_assessments:
		if assessment.accecpted_requests.filter(email=user.email).count()!=0:
			assessment_allowed.append(assessment)
	context={
		'all_assessments':assessment_allowed,
	}
	return render(request, 'quiz/all_assessments.html', context)

@login_required(login_url='/login')
def assessment_detail(request, assessment_no):
	user=request.user
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	context={
		'assessment':assessment,
	}
	if(not assessment.live  or assessment.accecpted_requests.filter(email=user.email).count()==0):
		return redirect('quiz:all_assessments')
	return render(request, 'quiz/assessment_detail.html',context)

@login_required(login_url='/login')
def assessment_start(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(not assessment.live):
		return redirect('quiz:all_assessments')
	questions=assessment.question_set.all()
	print(questions)
	now=datetime.datetime.now()
	end=now+datetime.timedelta(minutes=assessment.duration)
	if not Random_questions.objects.filter(user=request.user, assessment=assessment).exists():
		random_q=random.sample(list(range(questions.count())),assessment.no_of_questions)
		q=Random_questions(user=request.user,assessment=assessment)
		q.save()
		for i in random_q:
			q.random_ques.add(questions[i])
	questions_object=get_object_or_404(Random_questions,user=request.user,assessment=assessment)
	questions=questions_object.random_ques.all()
	if not timeRemaining.objects.filter(user=request.user, assessment=assessment).exists():
		t=timeRemaining(user=request.user, timeStart=now, timeEnd=end, assessment=assessment)
		t.save()
	return redirect('quiz:assessment_start_question', assessment.pk, questions[0].pk)

@login_required(login_url='/login')
def assessment_start_question(request, assessment_no, question_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(not assessment.live):
		return redirect('quiz:all_assessments')
	question=get_object_or_404(Question, pk=question_no)
	questions=assessment.question_set.all()
	if not Random_questions.objects.filter(user=request.user, assessment=assessment).exists():
		random_q=random.sample(list(range(questions.count())),assessment.no_of_questions)
		q=Random_questions(user=request.user,assessment=assessment)
		q.save()
		for i in random_q:
			q.random_ques.add(questions[i])
	questions_object=get_object_or_404(Random_questions,user=request.user,assessment=assessment)
	questions=questions_object.random_ques.all()
	flag=0
	next_question=question
	for i in questions:
		if(flag==1):
			next_question=i
			break
		if i==question:
			flag=1
	now=datetime.datetime.now()
	end=now+datetime.timedelta(minutes=assessment.duration)
	if not timeRemaining.objects.filter(user=request.user, assessment=assessment).exists():
		t=timeRemaining(user=request.user, timeStart=now, timeEnd=end, assessment=assessment)
		t.save()
	t=get_object_or_404(timeRemaining, user=request.user, assessment=assessment)
	now=t.timeStart
	end=t.timeEnd
	start_time=int(now.strftime("%s"))*1000
	end_time=int(end.strftime("%s"))*1000

	try:
		my_resp=Response.objects.get(question=question, assessment=assessment, user=request.user)
		my_resp=str(my_resp.response)
	except Response.DoesNotExist:
		my_resp='Z'
	
	if request.method=='POST':
		response=request.POST['optionsRadios']
		response_object=Response(
			user=request.user,
			assessment=assessment,
			question=question,
			response=response
		)
		try:
			prev_res=Response.objects.get(question=question, assessment=assessment, user=request.user)
			prev_res.response=response
		except Response.DoesNotExist:
			prev_res = response_object
		curr=datetime.datetime.now()
		if(timezone.now()<end):
			prev_res.save()
		else:
			return render(request, 'quiz/announcement.html', context={'message':"Time has expired!"})

		if(next_question==question):
			return redirect('quiz:assessment_finish', assessment.pk)
		return redirect('quiz:assessment_start_question', assessment.pk, next_question.pk)
	context={
		'questions':questions,
		'assessment':assessment,
		'start_time':start_time,
		'end_time':end_time,
		'curr_time':int(datetime.datetime.now().strftime("%s"))*1000,
		'question':question,
		'response':my_resp
	}
	return render(request, 'quiz/assessment_start.html', context)

@login_required(login_url='/login')
def assessment_finish(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(not assessment.live):
		return redirect('quiz:all_assessments')
	questions_object=get_object_or_404(Random_questions,user=request.user,assessment=assessment)
	questions=questions_object.random_ques.all()
	context={
		'assessment':assessment,
		'firstq':questions[0]
	}

	return render(request, 'quiz/assessment_finish.html', context)

@login_required(login_url='/login')
def assessment_finish_submit(request,assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(not assessment.live):
		return redirect('quiz:all_assessments')
	if assessment.conformation_mail==0:
		pass
	elif assessment.conformation_mail==1:
		email_message="Your response to " + assessment.name + " is recorded. You will hear about your scores shortly."
		emailSend("IIITD Exam Portal",request.user.email,email_message)
	elif assessment.conformation_mail==2:
		user_responses=Response.objects.filter(assessment=assessment, user=request.user)
		score=0
		for response in user_responses:
			if(response.question.solution==response.response):
				score=score+1
		email_message="You scored " +str(score)+" in "+ assessment.name + " out of "+ assessment.no_of_questions
		emailSend("IIITD Exam Portal",request.user.email,email_message)
	return redirect('quiz:home')

@login_required(login_url='/login')
def time_exp(request,assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(not assessment.live):
		return redirect('quiz:all_assessments')
	if assessment.conformation_mail==0:
		pass
	elif assessment.conformation_mail==1:
		email_message="Your response to " + assessment.name + " is recorded. You will hear about your scores shortly."
		emailSend("IIITD Exam Portal",request.user.email,email_message)
	elif assessment.conformation_mail==2:
		user_responses=Response.objects.filter(assessment=assessment, user=request.user)
		score=0
		for response in user_responses:
			if(response.question.solution==response.response):
				score=score+1
		email_message="You scored " +str(score)+" in "+ assessment.name + " out of "+ assessment.no_of_questions
		emailSend("IIITD Exam Portal",request.user.email,email_message)
	context={}
	return render(request, 'quiz/time_expired.html', context)
# Create Admin views here.

@staff_member_required
def admin_home(request):
	user=request.user

	status='Staff'
	context={
	'status':status,
	'user':user,
	}
	return render(request, 'quiz/admin_home.html', context)


@staff_member_required
def register_reqs(request):
	context={
		'register_reqs': registerRequests.objects.all(),
	}
	return render(request, 'quiz/register_reqs.html', context)

@staff_member_required
def approveRegister(request, request_no):
	req=get_object_or_404(registerRequests, pk=request_no)
	my_uname=req.e_mail
	my_uname_array=my_uname.split('@')
	userName=my_uname_array[0]
	new_user=User.objects.create_user(userName,first_name=req.first_name, last_name=req.last_name, password=req.password, email=req.e_mail)
	email_message="Your Account has been created:\nUsername = "+userName
	emailSend("IIITD-Online Quiz 	Account Activation",req.e_mail,email_message)
	new_user.save()
	req.delete()
	return redirect('quiz:register_reqs')

@staff_member_required
def disapproveRegister(request, request_no):
	req=get_object_or_404(registerRequests, pk=request_no)
	email_message="Your Account request has been Rejected"
	emailSend("IIITD-Online Quiz Account Activation Failed",req.e_mail,email_message)
	req.delete()
	return render(request, 'quiz/announcement.html', context={'message':"Dis Approved"})
@staff_member_required
def register_students(request):
	context={
	'assessments':Assessment.objects.all(),
	}
	return render(request,'quiz/register_students.html',context)
@staff_member_required
def viewAssessmentStudents(request,assessment_no):
	assessment=get_object_or_404(Assessment,pk=assessment_no)
	context={
	'assessment':assessment,
	'approved_request':assessment.accecpted_requests.all(),
	'pending_requests':assessment.pending_requests.all(),
	}
	if request.method=='POST':
		if request.FILES.get('excelfile',False):
			File=saveFile(assessment.name, request.FILES['excelfile'])
			path="/home/iiitd/Assessments/examiz2"
			print(urllib.unquote(File))		
			book = xlrd.open_workbook(path+urllib.unquote(File))
			sh = book.sheet_by_index(0)
			temp_name=""
			for rx in range(sh.nrows):
				for i in sh.row(rx):
					if str(i.value).find("@")>0:
						print (str(i.value))
						aUser=User.objects.filter(email=str(i.value))
						if len(aUser)>0:
							assessment.pending_requests.remove(aUser[0])
							assessment.accecpted_requests.add(aUser[0])
						else:
							temp_name=temp_name.split(' ')
							tmp=''
							for i1 in range(1,len(temp_name)):
								tmp=temp_name[i1]+" "
							my_uname=str(i.value)
							my_uname_array=my_uname.split('@')
							userName=my_uname_array[0]
							s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
							passlen = 8
							p =  "".join(random.sample(s,passlen ))
							new_user=User.objects.create_user(userName,first_name=temp_name[0], last_name=tmp, password=p, email=str(i.value))
							email_message="Your Account has been created:\nUsername = "+userName + ". Your password is "+ p +" ."
							emailSend("IIITD-Online Quiz 	Account Activation",str(i.value),email_message)
							new_user.save()
							assessment.accecpted_requests.add(new_user)
					else:
						temp_name=str(i.value)
			os.remove(path+urllib.unquote(File))

	return render(request,'quiz/viewAssessmentStudents.html',context)

@staff_member_required
def accept_test_request(request,assessment_no,user_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	user=get_object_or_404(User, pk=user_no)
	assessment.pending_requests.remove(user)
	assessment.accecpted_requests.add(user)
	email_message="You can now approved to give "+assessment.name
	emailSend("IIITD Exam Portal",user.email,email_message)
	return redirect('quiz:viewAssessmentStudents', assessment.pk)

@staff_member_required
def reject_test_request(request,assessment_no,user_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	user=get_object_or_404(User, pk=user_no)
	assessment.pending_requests.remove(user)
	return redirect('quiz:viewAssessmentStudents', assessment.pk)

def accepted_test_request(request,assessment_no):
	assessment=get_object_or_404(Assessment,pk=assessment_no)
	context={
	'assessment':assessment,
	'approved_requests':assessment.accecpted_requests.all(),
	'pending_requests':assessment.pending_requests.all(),
	}
	return render(request,'quiz/Accepted_sttudents_request.html',context)
	
@staff_member_required
def accept_all_test_request(request,assessment_no):
	assessment=get_object_or_404(Assessment,pk=assessment_no)
	pending_requests=assessment.pending_requests.all()
	for user in pending_requests:
		assessment.pending_requests.remove(user)
		assessment.accecpted_requests.add(user)
		email_message="You can now approved to give "+assessment.name
		emailSend("IIITD Exam Portal",user.email,email_message)
	return redirect('quiz:viewAssessmentStudents', assessment.pk)

@staff_member_required
def assessment(request):
	context={
		'assessments':Assessment.objects.all(),
	}
	return render(request,'quiz/assessment.html', context)

@staff_member_required
def createAssessment(request):
	context={}
	if request.method=='POST':
		name=request.POST['name']
		date=request.POST['date']
		max_marks=request.POST['max_marks']
		no_of_questions=request.POST['no_of_questions']
		duration=request.POST['duration']
		description=request.POST['description']
		conformation_mail=request.POST['Conformation_mail']

		assessment_object=Assessment(
			name=name,
			date=date,
			max_marks=max_marks,
			no_of_questions=no_of_questions,
			duration=duration,
			description=description,
			conformation_mail=conformation_mail,
		)
		assessment_object.save()
		return redirect('quiz:assessment')

	return render(request, 'quiz/create.html', context)


@staff_member_required
def viewAssessment(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	questions=assessment.question_set.all()
	context={
		'assessment':assessment,
		'questions':questions,
	}
	return render(request, 'quiz/view_assessment.html', context)

@staff_member_required
def assessment_live(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if(assessment.live):
		assessment.live=False
	else:
		assessment.live=True
	assessment.save()
	return redirect('quiz:viewAssessment', assessment.pk)
@staff_member_required
def createQuestion(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)

	context={
		'assessment': assessment,
	}
	if request.method=='POST':
		question=request.POST['question']
		option_a=request.POST['option_a']
		option_b=request.POST['option_b']
		try:
			option_c=request.POST['option_c']
		except:
			pass
		try:
			option_d=request.POST['option_d']
		except:
			pass
		try:
			option_e=request.POST['option_e']
		except:
			pass
		try:
			option_f=request.POST['option_f']
		except:
			pass
		try:
			option_g=request.POST['option_g']
		except:
			pass
		try:
			option_h=request.POST['option_h']
		except:
			pass	
		# question_image=None
		# option_a_image=None
		# option_b_image=None
		# option_c_image=None
		# option_d_image=None
		# print(request.FILES)
		if request.FILES.get('question_image',False):
			question_image=saveFile(assessment.name, request.FILES['question_image'])
		if request.FILES.get('option_a_image',False):
			option_a_image=saveFile(assessment.name, request.FILES['option_a_image'])
		if request.FILES.get('option_b_image',False):
			option_b_image=saveFile(assessment.name, request.FILES['option_b_image'])
		if request.FILES.get('option_c_image',False):
			option_c_image=saveFile(assessment.name, request.FILES['option_c_image'])
		if request.FILES.get('option_d_image',False):
			option_d_image=saveFile(assessment.name, request.FILES['option_d_image'])
		if request.FILES.get('option_e_image',False):
		 	option_e_image=saveFile(assessment.name, request.FILES['option_e_image'])
		
		if request.FILES.get('option_f_image',False):
		 	option_f_image=saveFile(assessment.name, request.FILES['option_f_image'])

		if request.FILES.get('option_g_image',False):
		 	option_g_image=saveFile(assessment.name, request.FILES['option_g_image'])

		if request.FILES.get('option_h_image',False):
		 	option_h_image=saveFile(assessment.name, request.FILES['option_h_image'])
		solution=request.POST['solution']

		question_object=Question(
			assessment=assessment,
			question=question,
			option_a=option_a,
			option_b=option_b,
			solution=solution,
		)
		try:
			question_object.option_c=option_c
		except:
			pass
		try:
			question_object.option_d=option_d
		except:
			pass
		try:
			question_object.option_e=option_e
		except:
			pass
		try:
			question_object.option_f=option_f
		except:
			pass
		try:
			question_object.option_g=option_g
		except:
			pass
		try:
			question_object.option_h=option_h
		except:
			pass	
		try:
			question_object.question_image=question_image
		except:
			pass
		try:
			question_object.option_a_image=option_a_image
		except:
			pass
		try:
			question_object.option_b_image=option_b_image
		except:
			pass
		try:
			question_object.option_c_image=option_c_image
		except:
			pass
		try:
			question_object.option_d_image=option_d_image
		except:
			pass
		try:
			question_object.option_e_image=option_e_image
		except:
			pass
		try:
			question_object.option_f_image=option_f_image
		except:
			pass
		try:
			question_object.option_g_image=option_g_image
		except:
			pass
		try:
			question_object.option_h_image=option_h_image
		except:
			pass
		question_object.save()
		return redirect('quiz:viewAssessment', assessment.pk)

	return render(request, 'quiz/question.html', context)


@staff_member_required
def viewQuestion(request, question_no):
	question=get_object_or_404(Question, pk=question_no)
	context={
		'question':question,
	}
	return render(request, 'quiz/view_question.html', context)

@staff_member_required
def editAssessment(request,assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	if request.method=='POST':
		name=request.POST['name']
		date=request.POST['date']
		max_marks=request.POST['max_marks']
		no_of_questions=request.POST['no_of_questions']
		duration=request.POST['duration']
		description=request.POST['description']
		conformation_mail=request.POST['Conformation_mail']

		assessment.name=name
		assessment.date=date
		assessment.max_marks=max_marks
		assessment.no_of_questions=no_of_questions
		assessment.duration=duration
		assessment.description=description
		assessment.conformation_mail=conformation_mail
		assessment.save()
		return redirect('quiz:assessment')
	date=str(assessment.date.year)+'-'
	if assessment.date.month<10:
		date=date+'0'+str(assessment.date.month)+'-'
	else:
		date=date+str(assessment.date.month)+'-'
	if assessment.date.day<10:
		date=date+'0'+str(assessment.date.day)
	else:
		date=date+str(assessment.date.day)

	context={
		'Assessment':assessment,
		'date':date,
	}
	return render(request,'quiz/editAssessment.html',context)

@staff_member_required
def deleteQuestion(request, question_no):
	question=get_object_or_404(Question,pk=question_no)
	responses=Response.objects.filter(question=question)
	for response in responses:
		response.delete()
	assessment=question.assessment
	question.delete()
	return redirect('quiz:viewAssessment', assessment.pk)

@staff_member_required
def evaluation(request):
	context={
		'assessments': Assessment.objects.all(),
	}
	return render(request,'quiz/evaluation.html', context)

@staff_member_required
def assessment_evaluate(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	responses=Response.objects.filter(assessment=assessment)
	users_list=[]
	for r in responses:
		users_list.append(r.user)
	users_list=list(set(users_list))
	marks=[]
	for user in users_list:
		user_responses=Response.objects.filter(assessment=assessment, user=user)
		count = 0
		for response in user_responses:
			if(response.question.solution==response.response):
				count+=1
		marks.append(count)
	users_marks=[]
	for u in range(len(users_list)):
		user_temp=[users_list[u],marks[u]]
		users_marks.append(user_temp)
	context={
		'assessment':assessment,
		'users_marks': users_marks,
	}
	return render(request,'quiz/assessment_evaluate.html', context)

@staff_member_required
def assessment_evaluate_user(request, assessment_no, user_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	user=get_object_or_404(User, pk=user_no)
	questions=assessment.question_set.all()
	responses=Response.objects.filter(assessment=assessment, user=user)
	count=0
	for response in responses:
		if(response.question.solution==response.response):
			count+=1
	percent=float(count)/(assessment.no_of_questions)*100

	context={
		'assessment':assessment,
		'user': user,
		'responses':responses,
		'percent':percent,
	}
	return render(request,'quiz/assessment_evaluate_user.html', context)
@staff_member_required
def assessment_evaluate_download(request,assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	responses=Response.objects.filter(assessment=assessment)
	users_list=[]
	for r in responses:
		users_list.append(r.user)
	users_list=list(set(users_list))
	excel=[["S.No.","Name","Email","Marks"]]
	num=1
	for u in users_list:
		user_responses=Response.objects.filter(assessment=assessment, user=u)
		count = 0
		for response in user_responses:
			if(response.question.solution==response.response):
				count+=1
		user_data=[num,str(u.first_name + " " + u.last_name),str(u.email),count]
		excel.append(user_data)
		num=num+1
	response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
	response['Content-Disposition'] = 'attachment; filename="marks.xlsx"'
	workbook  = xlsxwriter.Workbook(response, {'in_memory': True})
	worksheet = workbook.add_worksheet()
	for i in range(len(excel)):
		for j in range(len(excel[0])):
			worksheet.write(i, j, excel[i][j])
	workbook.close()
	return response
@staff_member_required
def assessment_evaluate_user_answers(request,assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)
	responses=Response.objects.filter(assessment=assessment)
	users_list=[]
	for r in responses:
		users_list.append(r.user)
	users_list=list(set(users_list))
	name=assessment.name
	path='/home/iiitd/Assessments/examiz2/result/'+name
	try:
		shutil.rmtree(path,ignore_errors=True)
	except:
		pass
	try:
		os.remove(name+'.zip')
	except:
		pass
	os.makedirs(path)
	for user in users_list:
		excel=[[str(user.first_name)+" "+str(user.last_name)," "," "],["Question","Student Response","Solution"]]
		user_name=str(user.first_name) + "_" +str(user.last_name)
		workbook = xlsxwriter.Workbook(path+'/'+user_name+".xlsx")
		worksheet = workbook.add_worksheet()
		user_responses=Response.objects.filter(assessment=assessment, user=user)
		for res in user_responses:
			temp=[]
			temp.append(res.question.question)
			temp.append(res.response)
			temp.append(res.question.solution)
			excel.append(temp)
		for i in range(len(excel)):
			for j in range(len(excel[0])):
				worksheet.write(i, j, excel[i][j])
		workbook.close()
	shutil.make_archive(name, 'zip', path)
	filename=name+'.zip'
	path2file='/home/iiitd/Assessments/examiz2/'+name+'.zip'
	zip_file = open(path2file, 'r')
	response = HttpResponse(zip_file, content_type='application/force-download')
	response['Content-Disposition'] = 'attachment; filename="%s"' % (filename)
	return response
