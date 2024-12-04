# appointments/views.py
#基本邏輯
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, Appointment, CustomUser
from django.utils.crypto import get_random_string
from datetime import datetime


# 登入邏輯
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

# 訊號處理邏輯
from django.db.models.signals import post_save
from django.dispatch import receiver
from billing.models import BillingRecord

@receiver(post_save, sender=Appointment)
def create_billing_record(sender, instance, created, **kwargs):
    if created:
        # 假設每次掛號都有固定費用
        BillingRecord.objects.create(appointment=instance, amount=100.00)


def index(request):
    return render(request, 'index.html')

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'description']  # 使用正確的字段

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # 傳入當前用戶
        super().__init__(*args, **kwargs)

        # 過濾醫師名單
        self.fields['doctor'].queryset = CustomUser.objects.filter(role='doctor')

        # 自動填充病患
        if user and user.role == 'patient':
            self.fields['description'].initial = f"Appointment requested by {user.full_name}"

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor')]
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    full_name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')], required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'role', 'full_name', 'age', 'gender']


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.full_name = form.cleaned_data['full_name']
            user.age = form.cleaned_data['age']
            user.gender = form.cleaned_data['gender']
            user.save()

            messages.success(request, 'Registration successful!')
            login(request, user)  # 自動登入
            return redirect('appointment_list')  # 根據角色跳轉頁面
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'appointments/register.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('login')  # 重導到登入頁面




# 掛號表單頁面
@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save(commit=False)
            # 自動設定病患為當前用戶
            patient = CustomUser.objects.get(username=request.user.username)
            appointment.patient = Patient.objects.get(name=patient.full_name)
            appointment.save()
            return redirect('appointment_list')
    else:
        form = AppointmentForm(user=request.user)

    return render(request, 'appointments/create.html', {'form': form})



# 掛號詳細頁面
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    patient_name = appointment.patient.name
    return render(request, 'appointments/detail.html', {'appointment': appointment, 'patient_name': patient_name})



# 掛號查詢頁面
@login_required
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()


        # 獲取篩選條件
    patient_name = request.GET.get('patient_name', '')  # 病患姓名
    doctor_name = request.GET.get('doctor_name', '')    # 醫生姓名

    # 查詢 Appointment 資料
    appointments = Appointment.objects.all()

    # 篩選條件
    if patient_name:
        appointments = appointments.filter(patient__name__icontains=patient_name)
    if doctor_name:
        appointments = appointments.filter(doctor__name__icontains=doctor_name)

    return render(request, 'appointments/list.html', {
        'appointments': appointments,
        'patient_name': patient_name,
        'doctor_name': doctor_name,
    })

from django.http import JsonResponse
from django.db.models import Q

def appointment_api(request):
    patient_name = request.GET.get('patient_name', '').strip()  # 去除兩側空白
    doctor_name = request.GET.get('doctor_name', '').strip()  # 去除兩側空白

    # 打印請求參數
    print(f"Received patient_name: {patient_name}, doctor_name: {doctor_name}")

    # 查詢 Appointment
    appointments = Appointment.objects.all()

    # 如果有提供篩選條件，則應用過濾器
    if patient_name:
        appointments = appointments.filter(patient__name__icontains=patient_name)
    if doctor_name:
        appointments = appointments.filter(doctor__name__icontains=doctor_name)

    # 返回 JSON 格式
    appointment_list = appointments.values(
        'appointment_id', 
        'patient__name', 
        'doctor__name', 
        'date', 
        'description'
    )
    return JsonResponse(list(appointment_list), safe=False)
