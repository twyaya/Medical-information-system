from django.contrib.auth.models import AbstractUser  # 引入自訂的 User 類別，繼承 Django 預設的 AbstractUser
from django.db import models  # 引入 Django 的 ORM 模型

# 自訂使用者模型，繼承自 AbstractUser
class User(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')  # 使用者的角色，預設為病患
    age = models.PositiveIntegerField(null=True, blank=True)  # 使用者的年齡（可選）
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)  # 性別

# 病人模型
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # 病患對應的使用者
    patient_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    dob = models.DateField()
    phone = models.CharField(max_length=15)

# 醫生模型
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)  # 醫生對應的使用者
    doctor_id = models.CharField(max_length=8, unique=True, null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

# 預約模型
class Appointment(models.Model):
    appointment_id = models.CharField(max_length=8, unique=True, null=True, blank=True)  # 預約的唯一識別碼，最多 8 個字元，可為空
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, db_column="patient_id")  # 外鍵，指向病人，當病人被刪除時，所有與其相關的預約也會被刪除
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, db_column="doctor_id")  # 外鍵，指向醫生，當醫生被刪除時，所有與其相關的預約也會被刪除
    date = models.DateTimeField()  # 預約的日期和時間
    description = models.TextField()  # 預約的描述，記錄病人或醫生的相關註解


# 公告模型
from django.utils.timezone import now

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="公告標題")
    content = models.TextField(verbose_name="公告內容")
    date = models.DateTimeField(default=now, verbose_name="公告日期")
    author = models.CharField(max_length=100, verbose_name="公告發布者")

    def __str__(self):
        return self.title
