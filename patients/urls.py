from django.urls import path
from .views import (
    get_patients,
    create_patient,
    get_patient,
    update_patient,
    delete_patient,
    get_patient_triage_history
)

urlpatterns = [
    path('patients/', get_patients),
    path('patients/create/', create_patient),
    path('patients/<int:pk>/', get_patient),
    path('patients/update/<int:pk>/', update_patient),
    path('patients/delete/<int:pk>/', delete_patient),
    path('patients/<int:pk>/triage-history/', get_patient_triage_history),
]