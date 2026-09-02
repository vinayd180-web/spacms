from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_live_class, name='create_live_class'),
    path('list/', views.live_class_list, name='live_class_list'),
    path('student/', views.student_live_classes, name='student_live_classes'),
    path('teacher/', views.teacher_live_classes, name='teacher_live_classes'),
]
