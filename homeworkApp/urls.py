from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_homework, name='teacher_homework'),
    path('student/', views.student_homework, name='student_homework'),
    path('admin/list/', views.admin_homework_list, name='admin_homework_list'),
]
