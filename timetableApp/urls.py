from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_timetable, name='student_timetable'),
    path('teacher/', views.teacher_timetable, name='teacher_timetable'),
    path('admin/list/', views.admin_timetable_list, name='admin_timetable_list'),
    path('admin/add/', views.admin_timetable_add, name='admin_timetable_add'),
]
