from django.urls import path
from .views import (
    PatientListView,
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
    get_patient_triage_history
)

urlpatterns = [
    path('', PatientListView.as_view(), name='patient-list'),
    path('create/', create_patient, name='patient-create'),
    path('<int:pk>/', get_patient, name='patient-detail'),
    path('update/<int:pk>/', update_patient, name='patient-update'),
    path('delete/<int:pk>/', delete_patient, name='patient-delete'),
    path('<int:pk>/triage-history/', get_patient_triage_history, name='patient-triage-history'),
]