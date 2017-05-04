import re
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from .models import CalendarEvent
from datetimewidget.widgets import DateTimeWidget
from multiupload.fields import MultiFileField
from datetime import datetime, timezone

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
    def clean(self):
        clean_data = super(CalendarEventForm, self).clean()
        start = clean_data.get('start')
        end = clean_data.get('end')
        if start and end:
            today = datetime.now(timezone.utc)
            if start < today:
                message = "You can't choose a start time before today!"
                self.add_error('start', forms.ValidationError(message))
            if end < today:
                message = "You can't choose a end time before today!"
                self.add_error('end', forms.ValidationError(message))
            if end < start:
                message = " You can't choose a end time before the start!"
                self.add_error('end', forms.ValidationError(message))



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
        def clean(self):
            clean_data = super(UpdateCalendarEventForm, self).clean()
            start = clean_data.get('start')
            end = clean_data.get('end')
            if start and end:
                today = datetime.now(timezone.utc)
                if start < today:
                    message = "You can't choose a start time before today!"
                    self.add_error('start', forms.ValidationError(message))
                if end < today:
                    message = "You can't choose a end time before today!"
                    self.add_error('end', forms.ValidationError(message))
                if end < start:
                    message = " You can't choose a end time before the start!"
                    self.add_error('end', forms.ValidationError(message))
