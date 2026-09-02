from django.urls import path
from . import views

urlpatterns = [
    path('mark_attendance', views.mark_attendance, name='mark_attendance'),
    path('teacher/', views.teacher_attendance, name='teacher_attendance'),
    path('admin/take/', views.admin_take_attendance, name='admin_take_attendance'),
    path('admin/mark/<int:class_id>/<str:date>/', views.admin_mark_attendance, name='admin_mark_attendance'),
    path('teacher/history/', views.teacher_attendance_history, name='teacher_attendance_history'),
    path('mark/<int:class_id>/', views.mark_attendance, name='mark_attendance'),
    path("student/<int:student_id>/history/", views.student_attendance_history, name="student_attendance_history"),
    path("attendance_list", views.admin_attendance_list, name="admin_attendance_list"),

]