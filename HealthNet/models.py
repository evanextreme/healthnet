from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
import datetime
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.



class Hospital(models.Model):
    hospitals = models.Manager()
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)



class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(null = True)
    date_of_birth = models.DateTimeField('Date of Birth', null=True)

    def __str__(self):
        name = self.first_name + " " + self.last_name
        return name


class Nurse(Person):
    nurses = models.Manager()
    employment_date = models.DateTimeField('Employment Date')
    employee_id = models.IntegerField()

    current_hospital_assignment = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )


class Doctor(Nurse):
    doctors = models.Manager()


class Patient(Person):
    patients = models.Manager()
    patient_id = models.IntegerField(null=True)
    doctor_notes = models.TextField()
    height = models.IntegerField()
    weight = models.IntegerField()

    @receiver(post_save, sender=User)
    def create_user_patient(sender, instance, created, **kwargs):
        if created:
            Patient.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_patient(sender, instance, **kwargs):
        instance.patient.save()

    doctor_assignment = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name ="doctor",
        null=True,
    )
    nurse_assignment = models.ForeignKey(
        Nurse,
        on_delete=models.CASCADE,
        related_name ="nurse",
        null=True,
    )
    current_hospital_assignment = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE,
        null = True,
    )





class Appointment(models.Model):
    date = models.DateTimeField()
    appointments = models.Manager()
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="attending_doctor"
    )
    nurse = models.ForeignKey(
        Nurse,
        on_delete=models.CASCADE,
        related_name ="attending_nurse"
    )
    notes = models.TextField()

    appointment_type = models.CharField(
        max_length=10,
    )
