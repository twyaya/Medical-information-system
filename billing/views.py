
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import models
from appointments.models import Appointment, Doctor
from .models import BillingRecord, Report
from django.db.models import Count, Sum

# Create your views here.
def index(request):
    return render(request, 'billing/index.html')

# 費用結算介面
def billing_interface(request):
    if request.method == 'POST':
        # 獲取更新的費用資料
        updates = request.POST.getlist('updates')
        for update in updates:
            appointment_id, new_amount = update.split(':')
            appointment = Appointment.objects.get(appointment_id=appointment_id)
            billing_record = BillingRecord.objects.get(appointment=appointment)
            billing_record.amount = float(new_amount)
            billing_record.save()

        return redirect('billing_interface')

    records = BillingRecord.objects.all()
    return render(request, 'billing/billing_interface.html', {'records': records})

# 報表生成功能
def generate_report(request):
    if request.method == 'POST':
        # 計算每位醫生的掛號數量
        appointment_counts = Appointment.objects.values('doctor__name').annotate(count=Count('id'))
        total_salaries = Doctor.objects.aggregate(total_salary=Sum('salary'))  # 假設 Doctor 模型有 salary 欄位

        report_data = {
            'appointment_counts': list(appointment_counts),
            'total_salaries': total_salaries['total_salary'],
        }

        report = Report.objects.create(report_name='Weekly Report', report_data=str(report_data))
        return redirect('report_list')

    return render(request, 'billing/generate_report.html')

def report_list(request):
    # 處理邏輯
    return render(request, 'billing/report_list.html')
