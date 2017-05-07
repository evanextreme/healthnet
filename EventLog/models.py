from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_delete
from django.core.exceptions import PermissionDenied
import jsonfield
from .signals import event_logged

class Log(models.Model):
    #the username of the user who acts
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        on_delete=models.SET_NULL
    )
    #the time of the action
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    #the abbreviation of the action
    action = models.CharField(max_length=50, db_index=True)
    #addtional notes if necessary
    notes = jsonfield.JSONField()

    #urls for each log
    @property
    def template_fragment_name(self):
        return "eventlog/{}.html".format(self.action.lower())
    
    #ordered by time
    class Meta:
        ordering = ["-timestamp"]
#
def log(user, action, notes=None):
        if (user is not None and not user.is_authenticated()):
            user = None
        if notes is None:
            notes = {}
        event = Log.objects.create(
            user=user,
            action=action,
            notes=notes
        )
        event_logged.send(sender=Log, event=event)
        return event

def log_delete(sender, instance, **kwargs):
    raise PermissionDenied
    
pre_delete.connect(log_delete,sender=Log)