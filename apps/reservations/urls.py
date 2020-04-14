from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.show_installations, name='index'),
    path('<str:sport>', views.filtered_installations, name='filtered_index'),
]