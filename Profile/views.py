from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from .form import patient_registration_form
from django.template import loader, Context
from django.contrib.auth import logout
from .form import *

def home(request):
	template = loader.get_template('main_page.html')
	variables = Context({'user':request.user})
	output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/login')

def register(request):
	if request.method == 'POST':
		form = patient_registration_form(request.POST)
		if form.is_valid():
			user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
			return HttpResponseRedirect('/')
	form = patient_registration_form()
	variables = RequestContext(request, {'form': form})
	return render_to_response('registration/register.html',variables)
	"""
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
	"""#return HttpResponse("At the registration page")

# Create your views here.
