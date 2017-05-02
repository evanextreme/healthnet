from django.contrib.auth.signals import user_logged_in, user_logged_out
from EventLog.models import log

def handle_login(sender, user, request, **kwargs):
    event=log(user=user,action="user_loggedin",notes={})
    event.save()

def handle_logout(sender, user, request, **kwargs):
    event=log(user=user,action="user_loggedout",notes={})
    event.save()

user_logged_in.connect(handle_login)
user_logged_out.connect(handle_logout)