from django.shortcuts import render
from django.http import HttpResponse
from HealthNet import models



def new_appt(request):
    return HttpResponse("new_appt.html")
