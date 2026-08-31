from django.shortcuts import render, redirect
from django.db import models
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Notification
from classesApp.models import ClassRoom
from studentsApp.models import Student

@login_required
def send_notification(request):
    classes = ClassRoom.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        message = request.POST.get('message')
        class_id = request.POST.get('class_room')
        is_for_all = request.POST.get('is_for_all') == 'on'

        if is_for_all:
            Notification.objects.create(
                title=title,
                message=message,
                is_for_all=True,
                created_by=request.user
            )
        else:
            Notification.objects.create(
                title=title,
                message=message,
                class_room_id=class_id,
                created_by=request.user
            )
        return redirect('send_notification')

    notifications = Notification.objects.all().order_by('-created_at')
    return render(request, 'notificationApp/send_notification.html', {
        'classes': classes,
        'notifications': notifications
    })

@login_required
def my_notifications(request):
    student = Student.objects.filter(user=request.user).first()
    if student:
        notifications = Notification.objects.filter(
            models.Q(is_for_all=True) | models.Q(class_room=student.class_room)
        ).order_by('-created_at')
    else:
        notifications = Notification.objects.filter(is_for_all=True).order_by('-created_at')

    return render(request, 'notificationApp/my_notifications.html', {'notifications': notifications})
