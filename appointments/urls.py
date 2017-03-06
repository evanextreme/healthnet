from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/$', views.new_appt, name='new_appt'),
    url(r'^create/$',views.create, name='create'),
]
