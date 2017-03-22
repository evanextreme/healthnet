from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page,name='register'),
	url(r'^profile/$', views.update_profile, name='profile'),
	url(r'^all_events/', views.all_events, name='all_events')
]