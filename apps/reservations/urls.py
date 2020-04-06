from django.contrib import admin
from django.urls import path
from apps.reservations import views

urlpatterns = [
    path('reservations/<int:pk_inst>/', views.reserve_day_hours, name='reservations'),
    path('', views.show_installations, name='index'),
]