from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from HealthNet.models import Appointment, Doctor, Patient
from datetime import date, time, datetime
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import AppointmentForm, CalendarEventForm


def new_appt(request):
    apptform = AppointmentForm()
    calform = CalendarEventForm()
    return render(request, 'appointments/new_appt2.html', {'apptform':apptform, 'calform':calform })


def create(request):
    if request.method == 'POST':
        apptform = AppointmentForm(request.POST)
        calform = CalendarEventForm(request.POST)

        if apptform.is_valid():
            apptform.save()
        if calform.is_valid():
            calform.save()
            return HttpResponse('Appointment Created!')
        else:
            return render(request, 'appointments/new_appt2.html', {'calform':calform, 'apptform':apptform})
