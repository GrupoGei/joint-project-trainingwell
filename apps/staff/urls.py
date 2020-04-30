from django.urls import path
from apps.staff import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]