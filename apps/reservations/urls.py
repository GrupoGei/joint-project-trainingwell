from django.urls import path
from apps.reservations import views
from django.contrib.auth import views as auth_views
from apps.reservations.forms import CustomAuthForm


urlpatterns = [
    path('show_installations/', views.show_installations, name='installations'),
    path('show_installations_reserved/<str:username>', views.show_installations_reserved, name='installations_reserved'),
    path('create/team/<int:pk_inst>', views.create_team, name='create_team'),
    path('show_reserves/<str:username>/', views.show_reserves, name='show_reserves'),
    path('show_reserves/<str:username>/sport/<str:sport>/', views.filtered_reserves, name='filtered_reserves'),
    path('reservations/<int:pk_inst>/date/<str:current_date>/event/<int:pk_event>', views.reserve_day_hours, name='reservations'),
    path('show_installations_reserved/<str:username>/checkout', views.checkout, name='checkout'),
    path('change_date/<int:pk_inst>/<int:pk_event>', views.change_date, name='change_date'),
    path('cancel_reserve/<int:pk_reserve>', views.delete_reserve, name='delete_reserve'),
    path('show_installations/<str:sport>', views.filtered_installations, name='filtered_index'),
    path('cancel_reserves_cart/<str:username>', views.cancel_reserves_cart, name='cancel_cart'),
    path('formalize_reserves/<str:username>', views.formalize_reserves, name='formalize_reserves'),
    path('login_success/', views.login_success, name='login_success'),
    path('create_event/<int:pk_inst>', views.create_event, name='create_event'),
    path('event/<int:pk_event>', views.event_detail, name='event_detail'),
    path('reserves/delete/<int:pk_reserve>', views.cancel_reserve, name='cancel-reserve'),
    path('', views.presentation_page, name='index'),
    path('current_planning/', views.current_planning, name='current_planning'),
    path('current_planning/<str:sport>/', views.filtered_events, name='filtered_events'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthForm), name='login'),
    path('logout/', views.logout_view, name='logout'),

]