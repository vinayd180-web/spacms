from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_quiz, name='create_quiz'),
    path('add-questions/<int:quiz_id>/', views.add_questions, name='add_questions'),
    path('import-questions/<int:quiz_id>/', views.import_questions, name='import_questions'),
    path('student/', views.student_quizzes, name='student_quizzes'),
    path('admin/results/', views.admin_quiz_results, name='admin_quiz_results'),
    path('take/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
]
