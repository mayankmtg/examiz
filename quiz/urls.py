from django.conf.urls import include, url
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^login/$', login, {'template_name':'accounts/login.html'}),
	url(r'logout$', logout, {'next_page': '/'}, name='logout'),
	url(r'^type_login/$', views.type_login, name='type_login'),

	#user side
	url(r'^user_home/$',views.user_home, name='user_home'),
	url(r'^register/$',views.register, name='register'),
	url(r'^all_assessments/$', views.all_assessments, name='all_assessments'),
	url(r'^apply_assessments/$', views.apply_assessments, name='apply_assessments'),
	url(r'^apply_assessments/(?P<assessment_no>\d+)/$', views.apply_request, name='apply_request'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/$',views.assessment_detail, name='assessment_detail'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/start$',views.assessment_start, name='assessment_start'),
	url(r'^assessment_detail/(?P<assessment_no>\d+)/(?P<question_no>\d+)$',views.assessment_start_question, name='assessment_start_question'),
	url(r'^assessment_finish/(?P<assessment_no>\d+)/$',views.assessment_finish, name='assessment_finish'),
	url(r'^assessment_finish/(?P<assessment_no>\d+)/submit$',views.assessment_finish_submit, name='assessment_finish_submit'),
	url(r'^assessment_finish/(?P<assessment_no>\d+)/time_exp/$',views.time_exp, name='time_exp'),
	url(r'^reset_password/$', password_reset, name='reset_password'),
	url(r'^reset_password/done/$', password_reset_done, name='password_reset_done'),
	url(r'^reset_password/complete/$', password_reset_complete, name='password_reset_complete'),
	url(r'^reset_password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name='password_reset_confirm'),

	#admin side
	url(r'^admin_home/$',views.admin_home, name='admin_home'),
	url(r'^register_reqs/$',views.register_reqs, name='register_reqs'),
	url(r'^register_students/$',views.register_students, name='register_students'),
	url(r'^approve/(?P<request_no>\d+)/$',views.approveRegister, name='approveRegister'), 
	url(r'^disapprove/(?P<request_no>\d+)/$',views.disapproveRegister, name='disapproveRegister'),
	url(r'^viewAssessmentStudents/(?P<assessment_no>\d+)/$',views.viewAssessmentStudents, name='viewAssessmentStudents'),
	url(r'^viewAssessmentStudents/(?P<assessment_no>\d+)/accept_all/$',views.accept_all_test_request, name='accept_all_test_request'),
	url(r'^viewAssessmentStudents/(?P<assessment_no>\d+)/accepted/$',views.accepted_test_request, name='accepted_test_request'),
	url(r'^viewAssessmentStudents/(?P<assessment_no>\d+)/(?P<user_no>\d+)/1$',views.accept_test_request, name='accept_test_request'),
	url(r'^viewAssessmentStudents/(?P<assessment_no>\d+)/(?P<user_no>\d+)/2$',views.reject_test_request, name='reject_test_request'),
	url(r'^assessment/$',views.assessment, name='assessment'),
	url(r'^create/$',views.createAssessment, name='createAssessment'),
	url(r'^view_assessment/(?P<assessment_no>\d+)/$',views.viewAssessment, name='viewAssessment'),
	url(r'^view_assessment/(?P<assessment_no>\d+)/edit/$',views.editAssessment, name='editAssessment'),
	url(r'^assessment_live/(?P<assessment_no>\d+)/$',views.assessment_live, name='assessment_live'),
	url(r'^create_question/(?P<assessment_no>\d+)/$',views.createQuestion, name='createQuestion'),
	url(r'^view_question/(?P<question_no>\d+)/$',views.viewQuestion, name='viewQuestion'),
	url(r'^view_question/(?P<question_no>\d+)/delete$',views.deleteQuestion, name='deleteQuestion'),
	url(r'^evaluation/$',views.evaluation, name='evaluation'),
	url(r'^evaluation/(?P<assessment_no>\d+)/$',views.assessment_evaluate, name='assessment_evaluate'),
	url(r'^evaluation/(?P<assessment_no>\d+)/download$',views.assessment_evaluate_download, name='assessment_evaluate_download'),
	url(r'^evaluation/(?P<assessment_no>\d+)/download_zip$',views.assessment_evaluate_user_answers, name='assessment_evaluate_user_answers'),
	url(r'^evaluation/(?P<assessment_no>\d+)/(?P<user_no>\d+)/$',views.assessment_evaluate_user, name='assessment_evaluate_user'),

]	

if True:
	urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
