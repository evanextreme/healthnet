import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from .models import CalendarEvent
from django.forms.extras.widgets import SelectDateWidget
from datetimewidget.widgets import DateTimeWidget




class CalendarEventForm(forms.ModelForm):

    class Meta:
        model = CalendarEvent
        fields = ['title','start','end','all_day']
        widgets = {
            #Use localization
            'start': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True),
            'end': DateTimeWidget(attrs={'id':"yourdatetimeid"}, usel10n = True),

            }
