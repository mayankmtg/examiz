from django.shortcuts import render, get_object_or_404
from .models import registerRequests
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


