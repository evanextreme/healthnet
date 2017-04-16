"""HealthNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from . import signals, views


urlpatterns = [
	url(r'^$', views.home, name='home'),
    url(r'^patients/$', views.patients, name='patients'),
    url(r'^patients/update$', views.employee_update_patient, name='employee_update_patient'),
    url(r'^patients/new_prescription/$', views.new_prescription, name='new_prescription'),
    url(r'^patients/employee_edit_prescription/$', views.employee_edit_prescription, name='employee_edit_prescription'),
    url(r'^appointments/new/$', views.new_appt, name='new_appt'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page,name='register'),
	url(r'^account/$', views.account, name='account'),
    url(r'^account/prescriptions/$', views.prescriptions, name='prescriptions'),
    url(r'^account/prescriptions/edit_prescription/$', views.edit_prescription, name='refill_prescription'),
	url(r'^account/profile/$', views.update_profile, name='profile'),
    url(r'^account/change_hospital/$', views.change_hospital, name='change_hospital'),
	url(r'^account/password/$', views.change_password, name='password'),
	url(r'^all_events/', views.all_events, name='all_events'),
    url(r'^export/', views.export_file, name='export_file'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doctor', views.doc_register_page,name='doc_register_page'),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
