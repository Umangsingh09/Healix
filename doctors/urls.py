from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.get_doctors, name='get_doctors'),
    path('recommend/', views.recommend_doctor, name='recommend_doctor'),
]