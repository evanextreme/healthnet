import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import CalendarEvent
from django.forms.extras.widgets import SelectDateWidget
from datetimewidget.widgets import DateTimeWidget
from HealthNet.models import Doctor



class CalendarEventForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.doctor.all(), empty_label=None)
    class Meta:
        model = CalendarEvent
        fields = ['title','start','end','all_day','doctor']
        widgets = {
            #Use localization
            'start': DateTimeWidget(attrs={'id':"yourdatetimeid1"}, usel10n = True),
            'end': DateTimeWidget(attrs={'id':"yourdatetimeid2"}, usel10n = True),
            #'end': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True),
            }
