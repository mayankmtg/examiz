from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage





from_user=settings.EMAIL_HOST_USER
def emailSend(subject, to_user, message):
	to_list=[]
	to_list.append(to_user)
	print(from_user, to_user)
	ret_val=send_mail(subject,message,from_user,to_list,fail_silently=False)
	return ret_val


def saveFile(assessment_name, myfile):
	fs = FileSystemStorage()
	filename = fs.save(assessment_name+"/"+myfile.name, myfile)
	uploaded_file_url = fs.url(filename)
	return uploaded_file_url