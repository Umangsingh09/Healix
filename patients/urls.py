from django.urls import path
from .views import (
    get_patients,
    create_patient,
    get_patient,
    update_patient,
    delete_patient
)

urlpatterns = [
    path('patients/', get_patients),
    path('patients/create/', create_patient),
    path('patients/<int:pk>/', get_patient),
    path('patients/update/<int:pk>/', update_patient),
    path('patients/delete/<int:pk>/', delete_patient),
]