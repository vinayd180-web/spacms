from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_worklog, name='teacher_worklog'),
    path('add/', views.add_worklog, name='add_worklog'),
    path('admin/list/', views.admin_worklog_list, name='admin_worklog_list'),
]
