from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from localflavor.us.models import PhoneNumberField

class Hospital(models.Model):
    hospitals = models.Manager()
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    def __str__(self):
        name = self.name
        return name


class Nurse(models.Model):
    # the Django user model holds user's name, email, username, password
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # date the employee was hired
    employment_date = models.DateTimeField(default=timezone.now)
    nurses = models.Manager()
    nurse_id = models.AutoField(primary_key=True)
    phone_number = PhoneNumberField()
    hospital = models.ForeignKey(Hospital)
    profile_picture = models.FileField(upload_to='nurses',blank=True)
    new_user = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    def self_card(self):
        variables = {'user':self.user}
        return(render_to_string('card/nurse.html',variables))


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.Manager()
    employment_date = models.DateTimeField(default=timezone.now)
    doctor_id = models.AutoField(primary_key=True)
    # phone number format XXX-XXX-XXXX
    phone_number = PhoneNumberField(default=None)
    # doctor can be employeed at multiple hospitals
    hospital = models.ManyToManyField(Hospital)
    # profile picture is a luxary feature
    profile_picture = models.FileField(upload_to='doctors',blank=True)
    # makes tap-target mini tutorial show if user is 'new'
    new_user = models.BooleanField(default=True)

    # Example "Dr. Paul Octoupus"
    def __str__(self):
        return str("Dr. " + self.user.first_name + " " + self.user.last_name)

    # Returns the doctor as a user object, for rendering him into a 'card' template
    def self_card(self):
        variables = {'user':self.user}
        return(render_to_string('card/doctor_self.html',variables))

    def card(self):
        variables = {'user':self.user}
        return(render_to_string('card/doctor.html',variables))



class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(default=timezone.now)
    patients = models.Manager()
    patient_id = models.AutoField(primary_key=True)
    phone_number = PhoneNumberField()
    # simple text notes. Example "Patient is contagious"
    doctor_notes = models.TextField(null=True)
    height = models.IntegerField()
    weight = models.IntegerField()
    # current assigned doctor (can only make appointments with this one)
    doctor = models.ForeignKey(Doctor)
    # patient's prefered hospital (possible for appointments to be in another)
    hospital = models.ForeignKey(Hospital)
    # true if a patient is staying in the hospital for an extended period
    admitted = models.BooleanField(default=False)
    discharge_date = models.DateTimeField(default=None, null=True)
    profile_picture = models.FileField(upload_to='patients',blank=True)
    new_user = models.BooleanField(default=True)

    # Example "Peter Parker"
    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

    def self_card(self):
        variables = {'user':self.user}
        return(render_to_string('card/patient_self.html',variables))

    def card(self):
        variables = {'user':self.user}
        return(render_to_string('card/patient.html',variables))

class Prescription(models.Model):
    prescriptions = models.Manager()
    # every Prescription gets assigned an auto ID
    prescription_id = models.AutoField(primary_key=True)
    # every Prescription needs a patient to take it
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    # i.e. "Ibuprofen", "Vicodin"
    drug_name = models.CharField(max_length=50)
    # i.e. 10mg 3x/day, 100mg 1x/day
    dosage = models.CharField(max_length=20)
    # i.e. "Take with food", ""
    instructions = models.TextField()
    # i.e. "May cause drowsieness"
    side_effects = models.TextField()
    # decremented when a patient refills
    refills_remaining = models.IntegerField()
    def __str__(self):
        drug_desc = str(self.drug_name + ' (' + self.dosage + ') ' + 'Refills Remaining: ' + str(self.refills_remaining))
        return drug_desc

    def refill(self):
        # decrement refills
        if self.refills_remaining < 0:
            return
        self.refills_remaining -=1
        return

class Export(models.Model):
    #
    user = models.OneToOneField(User)
    file = models.FileField(upload_to='exports',blank=True)
