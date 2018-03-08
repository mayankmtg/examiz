from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from . import views



urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^login/$', login, {'template_name':'accounts/login.html'}),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),

	#user side
	url(r'^register/$',views.register, name='register'),
	url(r'^all_assessments/$', views.all_assessments, name='all_assessments'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/$',views.assessment_detail, name='assessment_detail'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/start$',views.assessment_start, name='assessment_start'),

	#admin side
	url(r'^register_reqs/$',views.register_reqs, name='register_reqs'),
	url(r'^approve/(?P<request_no>\d+)/$',views.approveRegister, name='approveRegister'), 
	url(r'^disapprove/(?P<request_no>\d+)/$',views.disapproveRegister, name='disapproveRegister'),
	url(r'^assessment/$',views.assessment, name='assessment'),
	url(r'^create/$',views.createAssessment, name='createAssessment'),
	url(r'^view_assessment/(?P<assessment_no>\d+)/$',views.viewAssessment, name='viewAssessment'),
	url(r'^create_question/(?P<assessment_no>\d+)/$',views.createQuestion, name='createQuestion'),
	url(r'^view_question/(?P<question_no>\d+)/$',views.viewQuestion, name='viewQuestion'),
	

]	