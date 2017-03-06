from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.template import loader, Context
from django.contrib.auth import logout
from Profile.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
	template = loader.get_template('index.html')
	variables = Context({'user':request.user})
	output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_page(request):
	if request.method=='POST':
		form=RegistrationForm(request.POST)
		if form.is_valid():
			user=User.objects.create_user(username=form.cleaned_data['username'],
			password=form.cleaned_data['password'],email=form.cleaned_data['email'])
			return HttpResponseRedirect('/')
	form=RegistrationForm()
	variables=RequestContext(request,{'form':form})
	return render_to_response("registration/register.html",variables)