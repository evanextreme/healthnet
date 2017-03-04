from django.db import models
from django.contrib.auth.models import Appointment
from datetime import datetime
# Create your models here.

class Event(models.Model):
    title = models.CharField(u"Title", max_length=50)
    description = MarkdownTextField(u"D")
    comments = models.TextField(u"Comentarios")
    date = models.DateField()
    starts = models.TimeField(blank=True, null=True)
    ends = models.TimeField(blank=True, null=True)
    price = models.CharField(default="Entrada gratuita", max_length=50)
    venue = models.ForeignKey(Venue)
    category = models.ForeignKey(Category)
    picture = ResizedImageField(upload_to = upload_to_event, 
                                max_width=185, max_height=185, 
                                blank=True, null=True)
    
    status = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    
    class Meta:
        verbose_name = u"Evento"
        verbose_name_plural = u"Eventos"
        ordering = ['date','starts']
    
    def __unicode__(self):
        return self.title

