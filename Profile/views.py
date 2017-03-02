from django.shortcuts import render
from django.http import HttpResponse

def login(request):
	return HttpResponse("Hello, you're at the login page")

# Create your views here.
