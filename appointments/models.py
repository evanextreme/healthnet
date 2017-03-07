from django.db import models
from HealthNet.models import Doctor, Patient, Nurse

# Create your models here.
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

    APPT_TYPE_CHOICES = (
        ('test', 'Test'),
        ('surgery', 'Surgery'),
        ('checkup', 'Check Up'),
        (None, 'Misc')
    )
    appointment_type = models.CharField(
        choices=APPT_TYPE_CHOICES,
        max_length=10,
    )
