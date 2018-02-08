from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login
from . import views



urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'login/$', login, {'template_name':'accounts/login.html'}),
	url(r'logout$', auth_views.logout, {'next_page': '/'}, name='logout'),
]	