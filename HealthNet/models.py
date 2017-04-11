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
    nurses = models.Manager()
    #employment_date = models.DateTimeField('Employment Date')
    #employee_id = models.IntegerField()

    current_hospital_assignment = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctors = models.Manager()
    employment_date = models.DateTimeField(default=timezone.now)
    doctors = models.Manager()
    doctor_id = models.AutoField(primary_key=True)

    phone_number = PhoneNumberField()

    hospital = models.ForeignKey(Hospital)

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

    profile_picture = models.ImageField(upload_to='patients',blank=True)


#@receiver(post_save, sender=User)
def create_patient(sender, instance, created, **kwargs):
    if created:
        Patient.patients.create(user=instance)

#@receiver(post_save, sender=User)
def save_patient(sender, instance, **kwargs):
    instance.patient.save()
