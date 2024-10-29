from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('appointments/create/', views.appointment_create, name='appointment_create'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<str:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
]
