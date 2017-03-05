from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .form import patient_registration_form

def login(request):
	return HttpResponse("Hello, you're at the login page")

def register(request):
	if request.method == 'POST':
		form = patient_registration_form(request.POST)
		if form.is_valid():
			form.save()
			return
	args = {}
	args.update(csrf(request))
	args['form'] = patient_registration_form()
	print(args)
	return render(request, 'register.html', args)
	#return HttpResponse("At the registration page")

# Create your views here.
