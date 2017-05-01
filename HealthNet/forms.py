import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from HealthNet.models import *
from multiupload.fields import MultiFileField



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(label="Date of Birth")
    height = forms.IntegerField()
    weight = forms.IntegerField()
    height.label = 'Height (Inches)'
    weight.label = 'Weight (Pounds)'
    profile_picture = forms.ImageField(label="Upload a photo of yourself!", required=False)
    phone_number = forms.CharField(initial='+12345678900')
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'phone_number', 'height', 'weight', 'doctor', 'hospital', 'profile_picture']
    def clean(self):
        clean_data = super(PatientForm, self).clean()
        doctor = clean_data.get('doctor')
        hospital = clean_data.get('hospital')

        if doctor and hospital:
            if not hospital in doctor.hospital.all():
                message = str(doctor) + 'only works at: '
                i = 0
                for h in doctor.hospital.all():
                    i+=1
                for h in doctor.hospital.all():
                    i-=1
                    if i == 0:
                        message += str(h) + " "
                    else:
                        message += str(h) + ", "
                self.add_error('doctor', forms.ValidationError(message))

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['phone_number','hospital']

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'drug_name', 'dosage', 'side_effects', 'refills_remaining']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['email','first_name','last_name']

class UpdatePatientForm(forms.ModelForm):
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    height.label = 'Height (Inches)'
    weight.label = 'Weight (Pounds)'
    class Meta:
        model = Patient
        fields = ['phone_number','height', 'weight', 'doctor', 'hospital']

class EmployeeUpdatePatientForm(forms.ModelForm):
    patient_id = forms.IntegerField(widget=forms.HiddenInput())
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    height.label = 'Height (Inches)'
    weight.label = 'Weight (Pounds)'
    class Meta:
        model = Patient
        fields = ['height', 'weight','hospital','patient_id']
