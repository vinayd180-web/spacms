from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Homework
from classesApp.models import ClassRoom
from teachersApp.models import Teacher
from studentsApp.models import Student

@login_required
def teacher_homework(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    homeworks = Homework.objects.filter(teacher=teacher).order_by('-due_date')
    classes = teacher.assigned_class.all()
    if request.method == 'POST':
        Homework.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            subject=request.POST.get('subject'),
            class_room_id=request.POST.get('class_room'),
            teacher=teacher,
            due_date=request.POST.get('due_date'),
        )
        return redirect('teacher_homework')
    return render(request, 'homeworkApp/teacher_homework.html', {'homeworks': homeworks, 'classes': classes})

@login_required
def student_homework(request):
    student = get_object_or_404(Student, user=request.user)
    homeworks = Homework.objects.filter(class_room=student.class_room).order_by('-due_date')
    return render(request, 'homeworkApp/student_homework.html', {'homeworks': homeworks})

@staff_member_required
def admin_homework_list(request):
    homeworks = Homework.objects.select_related('class_room', 'teacher').all().order_by('-due_date')
    return render(request, 'homeworkApp/admin_homework_list.html', {'homeworks': homeworks})
