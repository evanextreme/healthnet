import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from HealthNet.models import Patient



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
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'height', 'weight', 'assigned_doctor', 'current_hospital_assignment']


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
        fields = ['height', 'weight', 'assigned_doctor', 'current_hospital_assignment']
