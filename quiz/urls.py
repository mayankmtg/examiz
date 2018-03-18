from django.conf.urls import include, url
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^home/$', views.home, name='home'),
	url(r'^login/$', login, {'template_name':'accounts/login.html'}),
	url(r'logout$', logout, {'next_page': '/'}, name='logout'),
	url('^', include('django.contrib.auth.urls')),

	#user side
	url(r'^register/$',views.register, name='register'),
	url(r'^all_assessments/$', views.all_assessments, name='all_assessments'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/$',views.assessment_detail, name='assessment_detail'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/start$',views.assessment_start, name='assessment_start'),
	url(r'^reset_password/$', password_reset, name='reset_password'),
	url(r'^reset_password/done/$', password_reset_done, name='password_reset_done'),
	url(r'^reset_password/complete/$', password_reset_complete, name='password_reset_complete'),
	url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),

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

if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)