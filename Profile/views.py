from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader, Context
from django.contrib.auth import logout
from Profile.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from eventlog.models import log
from HealthNet.models import *
from django.contrib.auth.models import User
from Calendar.models import CalendarEvent
from Calendar.util import events_to_json, calendar_options
from eventlog.models import log
from Calendar.forms import CalendarEventForm

def home(request):
	template = loader.get_template('index.html')
	variables = Context({'user':request.user})
	output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
    event = log(user=request.user, action="user_logout")
    event.save()
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def register_page(request):
    context = RequestContext(request)

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

            event = log(user=patient.user, action="patient_registration")
            event.save()
            response=HttpResponse()
            response.write("<h1>Congratulation! You are registered!</h1>")
            response.write("<h2>Please <a href='../login/'>log in</a>.</h2>")
            return response
        else:
            print(userform.errors, profileform.errors)
    else:
        userform=UserForm()
        patientform=PatientForm()
    variables=RequestContext(request,{'userform':userform, 'patientform':patientform})
    return render_to_response("registration/register.html",variables)

def update_profile(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST, instance = request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/')
		return render(request, 'profile.html', {
				'RegistrationForm': RegistrationForm
				})


    #user = User.objects.get(pk=user_id)
    #user.profile.name = 'elit'
    #user.save()

@csrf_exempt
def new_appt(request):
    if request.method == 'POST':
        cal_form = CalendarEventForm(request.POST)
        if cal_form.is_valid():
            appt = cal_form.save()
            appt.save()
            return render_to_response("index.html")

    else:
        cal_form = CalendarEventForm()
    variables=RequestContext(request,{'cal_form':cal_form})
    return render_to_response("appointments/new_appt.html",variables)


def all_events(request):
    events = CalendarEvent.objects.all()
    return HttpResponse(events_to_json(events), content_type='application/json')
