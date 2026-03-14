# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('triage/', views.triage_api, name='triage_api'),
    path('triage/stream/', views.triage_stream, name='triage_stream'),
    path('health/', views.health_check, name='health_check'),
]
