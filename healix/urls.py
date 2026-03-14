from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/', include('healix.api.urls')),
    path('api/patients/', include('patients.urls')),
    path('api/triage/', include('triage.urls')),
    path('api/doctors/', include('doctors.urls')),
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # Frontend URLs
    path('login/', RedirectView.as_view(url='/auth/login/', permanent=False), name='login_redirect'),
    path('auth/login/', TemplateView.as_view(template_name='auth/login.html'), name='login_ui'),
    path('triage/', TemplateView.as_view(template_name='patients/triage.html'), name='triage_ui'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/index.html'), name='dashboard_ui'),
    path('dashboard/doctor/', TemplateView.as_view(template_name='dashboard/doctor.html'), name='doctor_dashboard_ui'),
    path('dashboard/patient/', TemplateView.as_view(template_name='dashboard/patient.html'), name='patient_dashboard_ui'),
]