from django.contrib import admin
from .models import *

admin.site.register(Nurse)
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Prescription)
