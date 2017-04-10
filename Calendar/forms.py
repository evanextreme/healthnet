import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import CalendarEvent
from datetimewidget.widgets import DateTimeWidget
from HealthNet.models import Doctor



class CalendarEventForm(forms.ModelForm):
    #doctor = forms.ModelChoiceField(queryset=Doctor.doctor.all(), empty_label=None)
    appointment_id = forms.IntegerField()
    class Meta:
        model = CalendarEvent
        fields = ['title','start','end','all_day','doctor','patient','appointment_id']
        widgets = {
            #Use localization
            'start': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            'end': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            }
