from django.contrib import admin
from .models import Patient, Appointment, Doctor,User

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Doctor)
admin.site.register(User)