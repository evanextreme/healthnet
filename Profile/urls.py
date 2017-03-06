from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^', views.home, name='home'),
	url(r'^login/$',views.login_page),
	url(r'^logout/$', views.logout_page, name='logout'),
	url(r'^register/$', views.register, name='register')
]