from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from HealthNet.models import Appointment
from datetime import date, time, datetime
from django.utils import timezone

def new_appt(request):
    patients = models.Patient.patients.order_by('first_name')
    doctors = models.Doctor.doctors.order_by('first_name')
    return render(request, 'appointments/new_appt.html',
                    {'patients': patients, 'doctors': doctors})


def create(request):
    if request.method == 'POST':
        patient = request.POST.get('patient')
        doctor = request.POST.get('doctor')
        appointment_type = request.POST.get('appointment_type')
        date = request.POST.get('date')
        print(date)
        time = request.POST.get('time')
#        dtime = datetime.combine(date, time)
        A = Appointment(date= timezone.now(),
                        patient=patient,
                        doctor=doctor,
                        nurse=doctor,
                        appointment_type = appointment_type)
        A.save()
