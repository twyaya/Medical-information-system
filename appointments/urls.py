from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 首頁
    path('', views.index, name='index'),

    # 註冊頁面
    path('register/', views.register, name='register'),

    # 登入頁面
    path('login/', auth_views.LoginView.as_view(template_name='appointments/login.html'), name='login'),

    # 創建掛號
    path('appointments/create/', views.appointment_create, name='appointment_create'),

    # 顯示掛號列表
    path('appointments/', views.appointment_list, name='appointment_list'),

    # 顯示單個掛號詳情
    path('appointments/<str:appointment_id>/', views.appointment_detail, name='appointment_detail'),

    # API 查詢掛號
    path('api/appointments/', views.appointment_api, name='appointment_api'),
]
