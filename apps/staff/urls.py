from django.urls import path
from apps.staff import views

urlpatterns = [
    path('installations/', views.dashboard_installations, name='dashboard-installations'),
    path('installations/create', views.dashboard_create_installation, name='dashboard-create-installation'),
    path('reserves/', views.dashboard_reserves, name='dashboard-reserves'),
    path('reserves/delete/<int:pk_reserve>', views.dashboard_cancel_reserve, name='dashboard-cancel-reserve'),
    path('installations/<int:pk_inst>', views.dashboard_modify_installation, name='dashboard-modify-installation'),
    path('installations/delete/<int:pk_inst>', views.dashboard_delete_installation, name='dashboard-delete-installation'),
    path('installations/<str:sport>', views.dashboard_filtered_installations, name='dashboard-filtered-installations'),
    path('report/', views.dashboard_reports, name='dashboard-reports'),
    path('prices/', views.dashboard_manage_prices, name='dashboard-manage-prices'),
    path('prices/<int:pk_inst>', views.dashboard_modify_price, name='dashboard-installation-price'),
    path('prices/<str:sport>', views.dashboard_filtered_installations_prices, name='dashboard-filtered-installations-prices'),
    path('sport/create', views.dashboard_create_sport, name='dashboard-create-sport'),
    path('api-data/', views.get_data, name="api_data"),
    path('chart/', views.chart_view, name= "chart"),
]