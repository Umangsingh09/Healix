from django.urls import path
from . import views

urlpatterns = [
    path('analyze/', views.AnalyzeTriageView.as_view(), name='analyze'),
    path('stats/', views.TriageStatsView.as_view(), name='stats'),
    path('history/', views.TriageHistoryView.as_view(), name='history'),
]