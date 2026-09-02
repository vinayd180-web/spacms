from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import LiveClass
from classesApp.models import ClassRoom
from teachersApp.models import Teacher
from studentsApp.models import Student

@staff_member_required
def create_live_class(request):
    classes = ClassRoom.objects.all()
    teachers = Teacher.objects.select_related('user').all()
    if request.method == 'POST':
        LiveClass.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            class_room_id=request.POST.get('class_room'),
            teacher_id=request.POST.get('teacher'),
            meeting_link=request.POST.get('meeting_link'),
            date=request.POST.get('date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
        )
        return redirect('live_class_list')
    return render(request, 'liveClassApp/create_live_class.html', {'classes': classes, 'teachers': teachers})

@staff_member_required
def live_class_list(request):
    classes = LiveClass.objects.select_related('class_room', 'teacher').all().order_by('date', 'start_time')
    return render(request, 'liveClassApp/live_class_list.html', {'classes': classes})

@login_required
def student_live_classes(request):
    student = get_object_or_404(Student, user=request.user)
    classes = LiveClass.objects.filter(class_room=student.class_room).order_by('date', 'start_time')
    return render(request, 'liveClassApp/student_live_classes.html', {'classes': classes})

@login_required
def teacher_live_classes(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    classes = LiveClass.objects.filter(teacher=teacher).order_by('date', 'start_time')
    return render(request, 'liveClassApp/teacher_live_classes.html', {'classes': classes})
