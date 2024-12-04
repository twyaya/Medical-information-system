from django.contrib import admin
from .models import Patient, Appointment, Doctor,CustomUser

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(CustomUser)