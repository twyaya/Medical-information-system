from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='billing_index'),
    path('billing_interface/', views.billing_interface, name='billing_interface'),
    path('generate_report/', views.generate_report, name='generate_report'),
    path('report-list/', views.report_list, name='report_list'),
]
