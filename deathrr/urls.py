from django.urls import path, include
from . import views

app_name = 'deathrr'

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('filter_reports/', views.filter_reports_view, name="filter_reports"),
    #path('filter_reports_count/', views.filter_reports_count_view, name="filter_reports_count"),
    path('create_deceased_report/', views.create_deceased_report, name='create_deceased_report'),
    path('update_deceased_report/<int:pk>', views.update_deceased_report, name='update_deceased_report'),
    path('view_deceased_report/<int:pk>', views.view_deceased_report, name='view_deceased_report'),
    path('delete_deceased_report/<int:pk>', views.delete_report, name='delete_deceased_report'),
    path('delete_deceased_code/<int:d_pk>/<int:c_pk>', views.delete_deceased_code, name='delete_deceased_code'),
    path('add_code/<int:pk>', views.add_code, name='add_code'),
    path('download_count_reports', views.download_count_reports, name="download_count_reports"),
    path('download_detail_reports', views.download_detail_reports, name="download_detail_reports"),
]