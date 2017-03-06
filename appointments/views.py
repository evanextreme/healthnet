from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from HealthNet.models import Appointment, Doctor, Patient
from datetime import date, time, datetime
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from .forms import AppointmentForm


def new_appt(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            patient = form.data['patient']
            doctor = form.cleaned_data['doctor']
            nurse = form.cleaned_data['nurse']
            date = form.cleaned_data['date']
            notes = form.cleaned_data['notes']
            appointment_type = form.cleaned_data['appointment_type']
            a = Appointment(patient, doctor, nurse, date, notes, appointment_type)
            a.save()

    else:
        form = AppointmentForm()
    return render(request, 'appointments/new_appt.html', {'form':form})


def create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        patient = form.data['patient']
        doctor = form.data['doctor']
        nurse = form.data['nurse']
        date = form.data['date']
        
        notes = form.data['notes']
        appointment_type = form.data['appointment_type']
        a = Appointment(patient, doctor, nurse, date, notes, appointment_type)
        a.save()
    return HttpResponse("Appointment Created!")
