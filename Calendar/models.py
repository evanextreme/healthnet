# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from HealthNet.models import Doctor, Patient

class CalendarEvent(models.Model):
    """The event set a record for an
    activity that will be scheduled at a
    specified date and time.

    It could be on a date and time
    to start and end, but can also be all day.

    :param title: Title of event
    :type title: str.

    :param start: Start date of event
    :type start: datetime.

    :param end: End date of event
    :type end: datetime.

    :param all_day: Define event for all day
    :type all_day: bool.
    """

    appointment_id = models.AutoField(primary_key=True, default=None)
    title = models.CharField(_('Title'), blank=True, max_length=200)

    type = models.CharField(choices=(
    ('1', 'General'),
    ('2', 'Blood Report'),
    ('3', 'X-Ray'),
    ('4', 'MRI')
    ),max_length=4,default=1)

    start = models.DateTimeField(_('Start'))
    end = models.DateTimeField(_('End'))
    all_day = models.BooleanField(_('All day'), default=False)
    appointments = models.Manager()
    doctor = models.ForeignKey(Doctor, default=None)
    patient = models.ForeignKey(Patient, default=None)

    class Meta:
        verbose_name = _('Event')
        verbose_name_plural = _('Events')
    def __str__(self):
        return self.title
    def __unicode__(self):
        return self.title


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments')
    appointment = models.ForeignKey(CalendarEvent)
