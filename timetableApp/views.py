from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Timetable
from studentsApp.models import Student
from teachersApp.models import Teacher

@login_required
def student_timetable(request):
    student = get_object_or_404(Student, user=request.user)
    timetable = Timetable.objects.filter(class_room=student.class_room).order_by('day', 'period')
    return render(request, 'timetableApp/student_timetable.html', {'timetable': timetable})

@login_required
def teacher_timetable(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    timetable = Timetable.objects.filter(teacher=teacher).order_by('day', 'period')
    return render(request, 'timetableApp/teacher_timetable.html', {'timetable': timetable})

@staff_member_required
def admin_timetable_list(request):
    timetable = Timetable.objects.select_related('class_room', 'teacher').all().order_by('class_room', 'day', 'period')
    return render(request, 'timetableApp/admin_timetable_list.html', {'timetable': timetable})

@staff_member_required
def admin_timetable_add(request):
    if request.method == 'POST':
        Timetable.objects.create(
            class_room_id=request.POST.get('class_room'),
            day=request.POST.get('day'),
            period=request.POST.get('period'),
            subject=request.POST.get('subject'),
            teacher_id=request.POST.get('teacher'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        return redirect('admin_timetable_list')
    from classesApp.models import ClassRoom
    from teachersApp.models import Teacher
    classes = ClassRoom.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    return render(request, 'timetableApp/admin_timetable_add.html', {'classes': classes, 'teachers': teachers})
