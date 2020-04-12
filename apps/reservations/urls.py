from django.contrib import admin
from django.urls import path
from apps.reservations import views

urlpatterns = [
    path('show_installations/', views.show_installations, name='index'),
    path('show_installations_reserved/<str:username>', views.show_installations_reserved, name='installations_reserved'),
    path('reservations/<int:pk_inst>/date/<str:current_date>', views.reserve_day_hours, name='reservations'),
    path('change_date/<int:pk_inst>', views.change_date, name='change_date'),
]