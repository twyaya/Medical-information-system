# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, Appointment
from django.utils.crypto import get_random_string
from datetime import datetime


def index(request):
    context = {
        'range_list': range(1, 5)  # 將 range(1, 5) 傳遞給模板
    }
    return render(request, 'index.html', context)


# 掛號表單頁面
def appointment_create(request):
    if request.method == 'POST':
        patient_id = request.POST.get('patient_id')
        doctor_id = request.POST.get('doctor_id')
        date_str = request.POST.get('date')
        description = request.POST.get('description')
        
        # 轉換日期格式
        date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # 自動生成 appointment_id
        appointment_id = get_random_string(length=8, allowed_chars='0123456789')
        
        # 創建掛號記錄
        appointment = Appointment(
            appointment_id=appointment_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            date=date,
            description=description
        )
        appointment.save()
        
        return redirect('appointment_list')
    
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'appointments/create.html', {'patients': patients, 'doctors': doctors})

# 掛號查詢頁面
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    return render(request, 'appointments/list.html', {'appointments': appointments})

# 掛號詳細頁面
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/detail.html', {'appointment': appointment})