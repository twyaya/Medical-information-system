from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='appointments/login.html'), name='login'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<str:appointment_id>/', views.appointment_detail, name='appointment_detail'),
]
