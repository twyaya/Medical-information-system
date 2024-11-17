from django.contrib.auth.models import AbstractUser
from django.db import models

class Patient(models.Model):
    patient_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()  # Date of birth
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField(null=False, default=18)


class Doctor(models.Model):
    doctor_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField(null=False, default=18)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column="patient_id")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column="doctor_id")
    date = models.DateTimeField()
    description = models.TextField()

class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)