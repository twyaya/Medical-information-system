# appointments/views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, Doctor, Appointment
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # "patient" 或 "doctor"
        name = request.POST['name']
        dob = request.POST.get('dob', None)
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', 'M')
        age = request.POST.get('age', 18)

        # 創建 Django User
        user = User.objects.create_user(username=username, password=password)

        # 根據選擇的角色建立 Patient 或 Doctor 資料
        if role == 'patient':
            Patient.objects.create(
                patient_id=username,
                name=name,
                dob=dob,
                phone=phone,
                gender=gender,
                age=age
            )
        elif role == 'doctor':
            Doctor.objects.create(
                doctor_id=username,
                name=name,
                gender=gender,
                age=age
            )

        messages.success(request, 'Registration successful!')
        return redirect('login')

    return render(request, 'appointments/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('appointment_list')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'appointments/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = form.cleaned_data.get('role')
            if role == 'patient':
                Patient.objects.create(user=user, name=user.username)
            elif role == 'doctor':
                Doctor.objects.create(user=user, name=user.username)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

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
def appointment_list(request):
    appointments = Appointment.objects.select_related('patient', 'doctor').all()
    return render(request, 'appointments/list.html', {'appointments': appointments})

# 掛號詳細頁面
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, appointment_id=appointment_id)
    return render(request, 'appointments/detail.html', {'appointment': appointment})