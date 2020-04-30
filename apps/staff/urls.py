from django.urls import path
from apps.staff import views

urlpatterns = [
    path('installations/', views.dashboard_installations, name='dashboard-installations'),
    path('reserves/', views.dashboard_reserves, name='dashboard-reserves'),
    path('reserves/delete/<int:pk_reserve>', views.dashboard_cancel_reserve, name='dashboard-cancel-reserve')
]