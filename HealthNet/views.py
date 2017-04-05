from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader, Context
from django.contrib.auth import logout
from HealthNet.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from eventlog.models import log
from HealthNet.models import *
from django.contrib.auth.models import User
from Calendar.models import CalendarEvent
from Calendar.util import events_to_json, calendar_options
from Calendar.forms import CalendarEventForm
from django.contrib.auth.forms import PasswordChangeForm

def home(request):
    event_url = 'all_events/'
    variables = Context({'user':request.user,'calendar_config_options':calendar_options(event_url, OPTIONS)})
    return render_to_response('index.html',variables)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def register_page(request):
    
    if request.method=='POST':
        userform=UserForm(data=request.POST)
        patientform=PatientForm(data=request.POST)
        if userform.is_valid() and patientform.is_valid():
            user = userform.save(commit=False)
            user.set_password(user.password)
            user.save()

            patient = patientform.save(commit=False)
            patient.user = user
            patient.save()

            event = log(user=patient.user, action="user_registered")
            event.save()
            response=HttpResponse()
            #TODO fix response
            response.write("<h1>Congratulation! You are registered!</h1>")
            response.write("<h2>Please <a href='../login/'>log in</a>.</h2>")
            return response
        else:
            print(userform.errors, patientform.errors)
    else:
        userform=UserForm()
        patientform=PatientForm()
        variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
        return render_to_response("registration/register.html",variables)

@csrf_exempt
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        updateform = UpdateUserForm(request.POST, instance = user)
        if updateform.is_valid():
            updateform.save()
            event=log(user=user,action="user_updateprofile")
            event.save()
            return HttpResponseRedirect('/')
    else:
        updateform = UpdateUserForm(initial={
            'email':user.email,
            'first_name':user.first_name,
            'last_name':user.last_name,})
        variables = RequestContext(request, {'user':user,'update_form':updateform})
        return render_to_response('account/profile.html', variables)

@csrf_exempt
def change_password(request):
    user = request.user
    if request.method == 'POST':
        passform = PasswordChangeForm(user, request.POST)
        if passform.is_valid():
            user = passform.save()
            auth.update_session_auth_hash(request, user)
            event=log(user=user,action="user_updatepassword")
            event.save()
            return HttpResponseRedirect('/')
    else:
        passform = PasswordChangeForm(user)
        variables = RequestContext(request, {'user':user,'password_form':passform})
        return render_to_response('account/password.html', variables)


def account(request):
    user = request.user
    variables = RequestContext(request, {'user':user})
    return render_to_response('account/index.html', variables)

@csrf_exempt
def new_appt(request):
    user = request.user
    if request.method == 'POST':
        cal_form = CalendarEventForm(request.POST)
        if cal_form.is_valid():
            appt = cal_form.save(commit=False)
            appt.patient = user.patient
            appt.save()
            event=log(user=user,action="new_appt")
            event.save()
            return HttpResponseRedirect('/')
    else:
        cal_form = CalendarEventForm()
        variables=RequestContext(request,{'user':user,'cal_form':cal_form})
        return render_to_response("appointments/new.html",variables)

def all_events(request):
    user = request.user
    if hasattr(user, 'patient'):
        appointments = user.patient.calendarevent_set.all()
    elif hasattr(user, 'doctor'):
        appointments = user.doctor.calendarevent_set.all()
    return HttpResponse(events_to_json(appointments), content_type='application/json')


OPTIONS = """{  timeFormat: "H:mm",
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month,agendaWeek,agendaDay',
                },
                allDaySlot: false,
                firstDay: 0,
                weekMode: 'liquid',
                slotMinutes: 15,
                defaultEventMinutes: 30,
                minTime: 8,
                maxTime: 20,
                editable: true,

                eventClick: function(event, jsEvent, view) {
                    var title = prompt('Event Title:', event.title, { buttons: { Ok: true, Cancel: false} });
                    if (title){
                        event.title = title;
                        $('#calendar').fullCalendar('updateEvent',event);
                    }
                },
            }"""