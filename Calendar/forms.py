import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import CalendarEvent
from datetimewidget.widgets import DateTimeWidget
from multiupload.fields import MultiFileField

class CalendarEventForm(forms.ModelForm):
    #doctor = forms.ModelChoiceField(queryset=Doctor.doctor.all(), empty_label=None)
    attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5,required=False)
    class Meta:
        model = CalendarEvent
        fields = ['title','type','start','end','all_day','doctor','patient','hospital','attachments']
        widgets = {
            #Use localization
            'start': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            'end': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            }

class UpdateCalendarEventForm(forms.ModelForm):
    #doctor = forms.ModelChoiceField(queryset=Doctor.doctor.all(), empty_label=None)
    appointment_id = forms.IntegerField()
    attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5,required=False)
    class Meta:
        model = CalendarEvent
        fields = ['title','type','start','end','all_day','doctor','patient','hospital','appointment_id','attachments']
        widgets = {
            #Use localization
            'start': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            'end': DateTimeWidget(attrs={'class':"yourdatetime"}, usel10n = True),
            }
