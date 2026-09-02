from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_results, name='student_results'),
    path('report-card/', views.report_card, name='report_card'),
    path('admin/list/', views.admin_results_list, name='admin_results_list'),
    path('admin/add/', views.admin_add_result, name='admin_add_result'),
    path('admin/update/<int:result_id>/', views.admin_update_result, name='admin_update_result'),
]
