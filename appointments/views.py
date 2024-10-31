# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, Appointment,User
from django.utils.crypto import get_random_string
from datetime import datetime

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth.decorators import login_required

# 自訂的註冊表單
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor')]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role', 'age', 'gender']

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.age = form.cleaned_data['age']
            user.gender = form.cleaned_data['gender']
            user.save()

            messages.success(request, 'Registration successful!')
            login(request, user)  # 自動登入
            return redirect('appointment_list')  # 登入後重導到掛號列表頁面
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'appointments/register.html', {'form': form})


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
        
        # 轉換日期格式，datetime-local 的格式為 '%Y-%m-%dT%H:%M'
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        
        # 自動生成 appointment_id
        appointment_id = get_random_string(length=8, allowed_chars='0123456789')
        
        # 確認 patient 和 doctor 是否存在
        patient = get_object_or_404(Patient, patient_id=patient_id)
        doctor = get_object_or_404(Doctor, doctor_id=doctor_id)
        
        # 創建掛號記錄
        appointment = Appointment(
            appointment_id=appointment_id,
            patient=patient,    # 傳遞 patient 物件
            doctor=doctor,      # 傳遞 doctor 物件
            date=date,
            description=description
        )
        appointment.save()
        
        return redirect('appointment_list')
    
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    return render(request, 'appointments/create.html', {'patients': patients, 'doctors': doctors})

# 掛號查詢頁面
@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    return render(request, 'appointments/list.html', {'appointments': appointments})


# 掛號詳細頁面
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/detail.html', {'appointment': appointment})