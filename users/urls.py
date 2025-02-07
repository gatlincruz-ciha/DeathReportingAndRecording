from django.contrib import admin
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.login_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password', views.reset_password_view, name='reset_password'),
    path('reset_password_success', views.reset_password_successful_view, name='reset_password_success'),
]