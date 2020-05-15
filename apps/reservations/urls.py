from django.urls import path
from apps.reservations import views
from django.contrib.auth import views as auth_views
from apps.reservations.forms import CustomAuthForm

urlpatterns = [
    path('show_installations/', views.show_installations, name='index'),
    path('show_installations_reserved/<str:username>', views.show_installations_reserved, name='installations_reserved'),
    path('show_reserves/<str:username>', views.show_reserves, name='show_reserves'),
    path('reservations/<int:pk_inst>/date/<str:current_date>', views.reserve_day_hours, name='reservations'),
    path('show_installations_reserved/<str:username>/checkout', views.checkout, name='checkout'),
    path('change_date/<int:pk_inst>', views.change_date, name='change_date'),
    path('cancel_reserve/<int:pk_reserve>', views.delete_reserve, name='delete_reserve'),
    path('show_installations/<str:sport>', views.filtered_installations, name='filtered_index'),
    path('cancel_reserves_cart/<str:username>', views.cancel_reserves_cart, name='cancel_cart'),
    path('formalize_reserves/<str:username>', views.formalize_reserves, name='formalize_reserves'),
    path('login_success/', views.login_success, name='login_success'),
    path('', auth_views.LoginView.as_view(template_name='login.html', authentication_form=CustomAuthForm), name='login'),

]