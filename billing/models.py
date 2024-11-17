from django.db import models
from appointments.models import Appointment, Doctor

class BillingRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.appointment_id} - ${self.amount}"

class Report(models.Model):
    report_name = models.CharField(max_length=100)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_data = models.TextField()  # 可用於存儲生成的報表內容

    def __str__(self):
        return self.report_name