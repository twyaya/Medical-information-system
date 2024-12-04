from django.contrib.auth.models import AbstractUser  # 引入自訂的 User 類別，繼承 Django 預設的 AbstractUser
from django.db import models  # 引入 Django 的 ORM 模型

# 病人模型
class Patient(models.Model):
    patient_id = models.CharField(max_length=8, unique=True, null=True, blank=True)  # 病人的唯一識別碼，最多 8 個字元，可為空
    name = models.CharField(max_length=100)  # 病人的姓名，最多 100 個字元
    dob = models.DateField()  # 病人的出生日期
    phone = models.CharField(max_length=15)  # 病人的電話號碼，最多 15 個字元
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])  # 病人的性別，選擇男或女
    age = models.IntegerField(null=False, default=18)  # 病人的年齡，默認為 18

# 醫生模型
class Doctor(models.Model):
    doctor_id = models.CharField(max_length=8, unique=True, null=True, blank=True)  # 醫生的唯一識別碼，最多 8 個字元，可為空
    name = models.CharField(max_length=100)  # 醫生的姓名，最多 100 個字元
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])  # 醫生的性別，選擇男或女
    age = models.IntegerField(null=False, default=18)  # 醫生的年齡，默認為 18
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # 醫生的薪水，最大 10 位數字，其中 2 位小數，默認為 0.00

# 預約模型
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, unique=True, null=True, blank=True)  # 預約的唯一識別碼，最多 8 個字元，可為空
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column="patient_id")  # 外鍵，指向病人，當病人被刪除時，所有與其相關的預約也會被刪除
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column="doctor_id")  # 外鍵，指向醫生，當醫生被刪除時，所有與其相關的預約也會被刪除
    date = models.DateTimeField()  # 預約的日期和時間
    description = models.TextField()  # 預約的描述，記錄病人或醫生的相關註解

# 自訂使用者模型，繼承自 AbstractUser，擴展了角色功能
class CustomUser(AbstractUser):
    ROLE_CHOICES = [('patient', 'Patient'), ('doctor', 'Doctor')]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)  # 用戶姓名
