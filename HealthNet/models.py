from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.



class Hospital(models.Model):
    hospitals = models.Manager()
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    def __str__(self):
        name = self.name
        return name



class Nurse(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.Manager()
    employment_date = models.DateTimeField(default=timezone.now)
    nurses = models.Manager()
    nurse_id = models.AutoField(primary_key=True)

    phone_number = PhoneNumberField()

    hospital = models.ForeignKey(Hospital)

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)

    def card(self):
        variables = {'user':self.user}
        return(render_to_string('card/doctor.html',variables))


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.Manager()
    employment_date = models.DateTimeField(default=timezone.now)
    doctors = models.Manager()
    doctor_id = models.AutoField(primary_key=True)

    phone_number = PhoneNumberField(default=None)

    hospital = models.ManyToManyField(Hospital)

    def __str__(self):
        return str("Dr. " + self.user.first_name + " " + self.user.last_name)

    def card(self):
        variables = {'user':self.user}
        return(render_to_string('card/doctor.html',variables))


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(default=timezone.now)
    patients = models.Manager()
    patient_id = models.AutoField(primary_key=True)

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

    def card(self):
        variables = {'user':self.user}
        return(render_to_string('card/patient.html',variables))

    phone_number = PhoneNumberField()

    doctor_notes = models.TextField(null=True)
    height = models.IntegerField()
    weight = models.IntegerField()

    doctor = models.ForeignKey(Doctor)
    hospital = models.ForeignKey(Hospital)

    admitted = models.BooleanField(default=False)
    discharge_date = models.DateTimeField(default=None, null=True)

    profile_picture = models.FileField(upload_to='patients',blank=True)





class Prescription(models.Model):
    prescriptions = models.Manager()
    #every Prescription gets assigned an auto ID
    prescription_id = models.AutoField(primary_key=True)
    #every Prescription needs a patient to take it
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=False)
    #i.e. "Ibuprofen", "Vicodin"
    drug_name = models.CharField(max_length=50)
    #i.e. 10mg 3x/day, 100mg 1x/day
    dosage = models.CharField(max_length=10)
    #i.e. "Take with food", ""
    instructions = models.TextField()
    #i.e. "May cauase drowsieness"
    side_effects = models.TextField()
    #decremented when a patient refills
    refills_remaining = models.IntegerField()
    def __str__(self):
        drug_desc = str(self.drug_name + ' ' + self.dosage)
        return drug_desc

    def refill(self):
        #decrement refills
        refills_remaining -= 1
