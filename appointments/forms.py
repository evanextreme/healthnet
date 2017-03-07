from django import forms
from Calendar.models import CalendarEvent
from HealthNet.models import Doctor, Patient, Nurse
from .models import Appointment
from datetime import datetime
from django.forms import DateTimeField


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'start', 'end', 'all_day']


class AppointmentForm(forms.ModelForm):

    class Meta:
        model = Appointment
        fields = ['date','patient','doctor','nurse','notes']

    APPT_TYPE_CHOICES = (
        ('test', 'Test'),
        ('surgery', 'Surgery'),
        ('checkup', 'Check Up'),
        (None, 'Misc')
    )
    appointment_type = forms.ChoiceField(APPT_TYPE_CHOICES)
