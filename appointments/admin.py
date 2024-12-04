from django.contrib import admin
from .models import Patient, Appointment, Doctor,User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'age', 'gender')
    list_filter = ('role',)

admin.site.register(User, UserAdmin)
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
