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
from eventlog.models import Log
from HealthNet.models import *
from django.contrib.auth.models import User


def home(request):
	template = loader.get_template('index.html')
	variables = Context({'user':request.user})
	output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

@csrf_exempt
def register_page(request):
	if request.method=='POST':
		userform=UserForm(request.POST, instance=User)
		patientform=PatientForm(request.POST, instance=Patient)
		if userform.is_valid() and patientform.is_valid():
			userform.save()
			patientform.save()

			return HttpResponse("YOURE REGISTERED IM SO PROUD OF YOU <3")
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
	#else:
	return render(request, 'profile.html', {
		'RegistrationForm': RegistrationForm
	})

    #user = User.objects.get(pk=user_id)
    #user.profile.name = 'elit'
    #user.save()
