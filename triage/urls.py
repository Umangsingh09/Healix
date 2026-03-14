from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.AnalyzeTriageView.as_view(), name='analyze'),
    path('health-agent/', views.health_agent, name='health_agent'),
]