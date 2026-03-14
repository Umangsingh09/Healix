from django.urls import path
from .views import get_patients, create_patient

urlpatterns = [
    path('patients/', get_patients),
    path('patients/create/', create_patient),
]