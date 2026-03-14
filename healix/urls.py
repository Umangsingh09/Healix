from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home),
    path('admin/', admin.site.urls),
    path('api/', include('patients.urls')),
    path('api/triage/', include('triage.urls')),
]