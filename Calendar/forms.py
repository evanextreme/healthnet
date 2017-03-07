from django import forms
from HealthNet.models import Doctor, Patient, Nurse
from .models import CalendarEvent
from datetime import datetime
from django.forms import DateTimeField


class CalendarEventForm(forms.ModelForm):
    class Meta:
        model = CalendarEvent
        fields = ['title', 'start', 'end', 'all_day', 'doctor', 'nurse', 'patient']
