"""
URL configuration for MedicalInformationSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views  # 引入剛剛在根目錄 views.py 中的 redirect 函數

urlpatterns = [
    path('', views.redirect_to_appointments, name='home'),  # 將首頁導向到 appointments
    path('appointments/', include('appointments.urls')),  # 包含 appointments 應用的 URL
    path('billing/', include('billing.urls')),
    path('admin/', admin.site.urls),
]
