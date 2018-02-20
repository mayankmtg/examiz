from django.shortcuts import render, get_object_or_404
from .models import registerRequests, Assessment, Question
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

# Create User views here.

def home(request):
	context={}
	return render(request, 'quiz/home.html', context)


def register(request):
	context={}
	if request.method=='POST':
		first_name=request.POST['first_name']
		last_name=request.POST['last_name']
		e_mail=request.POST['email']
		password=request.POST['password']
		confirm_password=request.POST['confirm_password']
		if(password==confirm_password):
			r=registerRequests(first_name=first_name, last_name=last_name, e_mail=e_mail, password=password, confirm_password=confirm_password)
			r.save()
			return HttpResponse("Register request sent: <br> You will receive confirmation through email")
		else:
			return HttpResponse("Password Mismatch")
	return render(request, 'quiz/register.html', context)


# Create Admin views here.


@staff_member_required
def register_reqs(request):
	context={
		'register_reqs': registerRequests.objects.all(),
	}
	return render(request, 'quiz/register_reqs.html', context)

@staff_member_required
def approveRegister(request, request_no):
	req=get_object_or_404(registerRequests, pk=request_no)
	userName=req.first_name[0]+req.last_name[0]+str(req.pk)
	new_user=User.objects.create_user(userName,first_name=req.first_name, last_name=req.last_name, password=req.password, email=req.e_mail)
	new_user.save()
	req.delete()
	return redirect('quiz:register_reqs')

@staff_member_required
def disapproveRegister(request, request_no):
	req=get_object_or_404(registerRequests, pk=request_no)
	req.delete()
	return HttpResponse("Dis Approved")

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

		assessment_object=Assessment(
			name=name,
			date=date,
			max_marks=max_marks,
			no_of_questions=no_of_questions,
			duration=duration,
			description=description,
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
def createQuestion(request, assessment_no):
	assessment=get_object_or_404(Assessment, pk=assessment_no)

	context={
		'assessment': assessment,
	}
	if request.method=='POST':
		question=request.POST['question']
		option_a=request.POST['option_a']
		option_b=request.POST['option_b']
		option_c=request.POST['option_c']
		option_d=request.POST['option_d']
		solution=request.POST['solution']

		question_object=Question(
			assessment=assessment,
			question=question,
			option_a=option_a,
			option_b=option_b,
			option_c=option_c,
			option_d=option_d,
			solution=solution,
		)
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
