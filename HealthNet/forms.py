import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from HealthNet.models import *
from multiupload.fields import MultiFileField
from django.core.validators import RegexValidator
from localflavor.us.forms import USPhoneNumberField
from input_mask.contrib.localflavor.br.widgets import BRPhoneNumberInput

import datetime



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
    phone_number = USPhoneNumberField()
    phone_number.label = 'Phone Number (Format: 123-456-7890)'
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'phone_number', 'height', 'weight', 'doctor', 'hospital', 'profile_picture']
    def clean(self):
        clean_data = super(PatientForm, self).clean()
        doctor = clean_data.get('doctor')
        height = clean_data.get('height')
        weight = clean_data.get('weight')
        hospital = clean_data.get('hospital')
        date_of_birth = clean_data.get('date_of_birth')

        if date_of_birth:
            today = datetime.datetime.now().date()
            if today < date_of_birth:
                message = 'Date of birth cannot be after today!'
                self.add_error('date_of_birth', forms.ValidationError(message))
        if height and weight:
            if height <=0:
                message = 'Height cannot be negative'
                self.add_error('height', forms.ValidationError(message))
            if weight <=0:
                message = 'Weight cannot be negative'
                self.add_error('weight', forms.ValidationError(message))
        if doctor and hospital:
            if not hospital in doctor.hospital.all():
                message = str(doctor) + ' only works at: '
                num_of_hospitals = doctor.hospital.all().count()
                for h in doctor.hospital.all():
                    if num_of_hospitals == 1:
                        message += str(h) + "."
                    else:
                        message += str(h) + ", "
                    num_of_hospitals -= 1
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
        fields = ['phone_number','height', 'weight']

class EmployeeUpdatePatientForm(forms.ModelForm):
    patient_id = forms.IntegerField(widget=forms.HiddenInput())
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
    height.label = 'Height (Inches)'
    weight.label = 'Weight (Pounds)'
    class Meta:
        model = Patient
        fields = ['height', 'weight','hospital','doctor_notes','patient_id']
