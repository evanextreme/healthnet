from django import forms
from HealthNet.models import Patient
from django.contrib.auth.forms import UserCreationForm

class patient_registration_form(UserCreationForm):
    username = forms.CharField(required = True)
    first_name = forms.CharField(required = True)
    last_name = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    date_of_birth = forms.DateTimeField(required = True)

    class Meta:
        model = Patient
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit = True):
        user = super(patient_registration_form,self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.date_of_birth = self.cleaned_date['date_of_birth']

        if commit:
            user.save()

        return user