from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()  # Date of birth
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField(null=False, default=18)


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])
    age = models.IntegerField(null=False, default=18)


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    description = models.TextField()
