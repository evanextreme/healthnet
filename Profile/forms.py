import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from HealthNet.models import Patient



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['date_of_birth']
