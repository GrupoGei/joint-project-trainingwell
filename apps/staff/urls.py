from django.urls import path
from apps.staff import views

urlpatterns = [
    path('installations/', views.dashboard_installations, name='dashboard-installations'),
    path('installations/create', views.dashboard_create_installation, name='dashboard-create-installation'),
    path('reserves/', views.dashboard_reserves, name='dashboard-reserves'),
    #path('reserves/<str:username>', views.dashboard_filtered_organizers, name='dashboard-filter-organizer'),
    path('reserves/delete/<int:pk_reserve>', views.dashboard_cancel_reserve, name='dashboard-cancel-reserve'),
    path('installations/<int:pk_inst>', views.dashboard_modify_installation, name='dashboard-modify-installation'),
    path('installations/delete/<int:pk_inst>', views.dashboard_delete_installation, name='dashboard-delete-installation'),
    path('installations/<str:sport>', views.dashboard_filtered_installations, name='dashboard-filtered-installations'),
]