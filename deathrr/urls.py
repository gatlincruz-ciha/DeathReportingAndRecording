from django.urls import path, include
from . import views

app_name = 'deathrr'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('code_range_home', views.range_home_view, name="range_home"),
    path('filter_reports/', views.filter_reports_view, name="filter_reports"),
    path('filter_range_reports/', views.filter_range_reports_view, name="filter_range_reports"),
    path('create_deceased_report/', views.create_deceased_report, name='create_deceased_report'),
    path('update_deceased_report/<int:pk>/<str:return_screen>', views.update_deceased_report, name='update_deceased_report'),
    path('view_deceased_report/<int:pk>/<str:return_screen>', views.view_deceased_report, name='view_deceased_report'),
    path('delete_deceased_report/<int:pk>/<str:return_screen>', views.delete_report, name='delete_deceased_report'),
    path('delete_deceased_code/<int:d_pk>/<int:c_pk>', views.delete_deceased_code, name='delete_deceased_code'),
    path('add_code/<int:pk>', views.add_code, name='add_code'),
    path('download_count_reports', views.download_count_reports, name="download_count_reports"),
    path('download_detail_reports', views.download_detail_reports, name="download_detail_reports"),
    path('find_code', views.find_and_add_icd_code, name='find_and_add_code')
]