from django.contrib import admin
from django.urls import path
from apps.reservations import views

urlpatterns = [
    path('reservations/', views.reserve_day_hours, name='reservations'),
    path('', views.show_installations, name='index'),
]