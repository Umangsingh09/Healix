from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.AnalyzeTriageView.as_view(), name='analyze_triage'),
]