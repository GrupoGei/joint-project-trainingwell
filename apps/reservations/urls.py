from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('show_installations/', views.show_installations, name='index'),
    #path('', views.show_installations_reserved, name='index'),
    #path('', views.show_installations, name='index'),
]
