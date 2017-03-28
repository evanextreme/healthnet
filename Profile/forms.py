import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from HealthNet.models import Patient



class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']

class PatientForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Patient
        fields = ['date_of_birth']

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    conf_pword = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), label='New Password')


    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password']
