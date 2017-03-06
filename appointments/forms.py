from django import forms
from HealthNet.models import Doctor, Patient, Appointment, Nurse



class AppointmentForm(forms.Form):
    patient = forms.ModelChoiceField(queryset=Patient.patients.all(), empty_label="None", label="Patient")
    doctor = forms.ModelChoiceField(queryset=Doctor.doctors.all(), empty_label="None", label="Doctor")
    nurse = forms.ModelChoiceField(queryset=Nurse.nurses.all(), empty_label="None", label="Nurse")
    date = forms.DateField(label="Date")
    notes = forms.CharField(label='Notes')

    APPT_TYPE_CHOICES = (
        ('test', 'Test'),
        ('surgery', 'Surgery'),
        ('checkup', 'Check Up'),
        (None, 'Misc')
    )
    appointment_type = forms.ChoiceField(APPT_TYPE_CHOICES)
