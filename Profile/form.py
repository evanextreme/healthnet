from django import forms
from HealthNet.models import Patient
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
#from django.contrib.auth.forms import UserCreationForm

class patient_registration_form(forms.Form):
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Password',
                          widget=forms.PasswordInput())
    password2 = forms.CharField(label='Password (Again)',
                        widget=forms.PasswordInput())

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain alphanumeric characters and the underscore.')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken.')
    """first_name = forms.CharField(required = True)
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

        return user"""