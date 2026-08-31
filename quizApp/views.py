from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Quiz, Question, QuizResult
from classesApp.models import ClassRoom
from studentsApp.models import Student

@staff_member_required
def create_quiz(request):
    classes = ClassRoom.objects.all()
    if request.method == 'POST':
        quiz = Quiz.objects.create(
            title=request.POST.get('title'),
            subject=request.POST.get('subject'),
            class_room_id=request.POST.get('class_room'),
            created_by=request.user,
            time_limit=request.POST.get('time_limit', 30),
        )
        return redirect('add_questions', quiz_id=quiz.id)
    return render(request, 'quizApp/create_quiz.html', {'classes': classes})

@staff_member_required
def add_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        Question.objects.create(
            quiz=quiz,
            question_text=request.POST.get('question_text'),
            option_a=request.POST.get('option_a'),
            option_b=request.POST.get('option_b'),
            option_c=request.POST.get('option_c'),
            option_d=request.POST.get('option_d'),
            correct_answer=request.POST.get('correct_answer'),
            marks=request.POST.get('marks', 1),
        )
        return redirect('add_questions', quiz_id=quiz.id)
    questions = Question.objects.filter(quiz=quiz)
    return render(request, 'quizApp/add_questions.html', {'quiz': quiz, 'questions': questions})

@login_required
def student_quizzes(request):
    student = get_object_or_404(Student, user=request.user)
    quizzes = Quiz.objects.filter(class_room=student.class_room)
    results = QuizResult.objects.filter(student=request.user)
    return render(request, 'quizApp/student_quizzes.html', {'quizzes': quizzes, 'results': results})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if QuizResult.objects.filter(quiz=quiz, student=request.user).exists():
        return render(request, 'quizApp/already_taken.html')
    questions = Question.objects.filter(quiz=quiz)
    if request.method == 'POST':
        score = 0
        total_marks = 0
        for question in questions:
            total_marks += question.marks
            selected = request.POST.get(f'question_{question.id}')
            if selected == question.correct_answer:
                score += question.marks
        percentage = (score / total_marks * 100) if total_marks else 0
        QuizResult.objects.create(
            quiz=quiz,
            student=request.user,
            score=score,
            total_marks=total_marks,
            percentage=percentage,
        )
        return render(request, 'quizApp/quiz_result.html', {
            'score': score,
            'total_marks': total_marks,
            'percentage': percentage,
        })
    return render(request, 'quizApp/take_quiz.html', {'quiz': quiz, 'questions': questions})

import csv
import io

@staff_member_required
def import_questions(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        # Paste mode
        if request.POST.get('paste_mode'):
            text = request.POST.get('questions_text')
            lines = text.strip().split('\n')
            for line in lines:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) >= 6:
                    Question.objects.create(
                        quiz=quiz,
                        question_text=parts[0],
                        option_a=parts[1],
                        option_b=parts[2],
                        option_c=parts[3],
                        option_d=parts[4],
                        correct_answer=parts[5].upper(),
                        marks=int(parts[6]) if len(parts) > 6 else 1,
                    )
            return redirect('add_questions', quiz_id=quiz.id)
        
        # File upload mode
        elif request.FILES.get('file'):
            file = request.FILES['file']
            decoded = file.read().decode('utf-8')
            reader = csv.reader(io.StringIO(decoded))
            for row in reader:
                if len(row) >= 6:
                    Question.objects.create(
                        quiz=quiz,
                        question_text=row[0],
                        option_a=row[1],
                        option_b=row[2],
                        option_c=row[3],
                        option_d=row[4],
                        correct_answer=row[5].upper(),
                        marks=int(row[6]) if len(row) > 6 else 1,
                    )
            return redirect('add_questions', quiz_id=quiz.id)
    
    return render(request, 'quizApp/import_questions.html', {'quiz': quiz})

@staff_member_required
def admin_quiz_results(request):
    results = QuizResult.objects.select_related('quiz', 'student').all().order_by('-submitted_at')
    return render(request, 'quizApp/admin_quiz_results.html', {'results': results})
