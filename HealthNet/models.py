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
    doctor = models.Manager()
    #employment_date = models.DateTimeField('Employment Date')
    #employee_id = models.AutoField(primary_key=True)
    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)
    current_hospital_assignment = models.ForeignKey(
        Hospital,
        on_delete=models.CASCADE
    )

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(default=timezone.now, blank=True)
    patients = models.Manager()
    #appointments = models.ManyToManyField(CalendarEvent)
    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)
    """
    doctor_notes = models.TextField()
    height = models.IntegerField()
    weight = models.IntegerField()

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
    """

#@receiver(post_save, sender=User)
def create_patient(sender, instance, created, **kwargs):
    if created:
        Patient.patients.create(user=instance)

#@receiver(post_save, sender=User)
def save_patient(sender, instance, **kwargs):
    instance.patient.save()
