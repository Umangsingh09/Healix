from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('api/', include('healix.api.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/triage/', include('triage.urls')),
    path('auth/login/', TemplateView.as_view(template_name='auth/login.html'), name='login_ui'),
    path('triage/', TemplateView.as_view(template_name='patients/triage.html'), name='triage_ui'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/index.html'), name='dashboard_ui'),
    path('dashboard/doctor/', TemplateView.as_view(template_name='dashboard/doctor.html'), name='doctor_dashboard_ui'),
    path('dashboard/patient/', TemplateView.as_view(template_name='dashboard/patient.html'), name='patient_dashboard_ui'),
]