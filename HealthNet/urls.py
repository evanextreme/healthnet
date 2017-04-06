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
	url(r'^appointments/new/$', views.new_appt, name='new_appt'),
    url(r'^appointments/update/$', views.update_appointment, name='update_appointment'),
	url(r'^login/$', auth_views.login, name='login'),
	url(r'^logout/$', views.logout_page, name='logout'),
    url(r'^register/$', views.register_page,name='register'),
	url(r'^account/$', views.account, name='account'),
	url(r'^account/profile/$', views.update_profile, name='profile'),
	url(r'^account/password/$', views.change_password, name='password'),
	url(r'^all_events/', views.all_events, name='all_events'),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
