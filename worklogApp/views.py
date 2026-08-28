from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import WorkLog
from teachersApp.models import Teacher
from classesApp.models import ClassRoom
from datetime import datetime

@login_required
def teacher_worklog(request):
    teacher = Teacher.objects.get(user=request.user)
    worklogs = WorkLog.objects.filter(teacher=teacher).order_by('-date')
    return render(request, 'worklogApp/teacher_worklog.html', {'worklogs': worklogs})

@login_required
def add_worklog(request):
    teacher = Teacher.objects.get(user=request.user)
    classes = ClassRoom.objects.all()
    if request.method == 'POST':
        WorkLog.objects.create(
            teacher=teacher,
            date=request.POST.get('date'),
            in_time=request.POST.get('in_time'),
            out_time=request.POST.get('out_time'),
            class_room_id=request.POST.get('class_room'),
            subject=request.POST.get('subject'),
            syllabus_covered=request.POST.get('syllabus_covered'),
        )
        return redirect('teacher_worklog')
    return render(request, 'worklogApp/add_worklog.html', {'classes': classes})

@staff_member_required
def admin_worklog_list(request):
    worklogs = WorkLog.objects.select_related('teacher', 'class_room').all().order_by('-date')
    return render(request, 'worklogApp/admin_worklog_list.html', {'worklogs': worklogs})
