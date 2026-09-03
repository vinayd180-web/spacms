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
    from django.db.models import Sum
    from datetime import date, timedelta
    today = date.today()
    month_start = today.replace(day=1)
    monthly_logs = WorkLog.objects.filter(teacher=teacher, date__gte=month_start)
    total_hours = monthly_logs.aggregate(Sum('hours_worked'))['hours_worked__sum'] or 0
    total_days = monthly_logs.count()
    syllabus_subjects = monthly_logs.values('subject').distinct()
    return render(request, 'worklogApp/teacher_worklog.html', {
        'worklogs': worklogs,
        'total_hours': total_hours,
        'total_days': total_days,
        'monthly_logs': monthly_logs,
    })

@login_required
def add_worklog(request):
    teacher = Teacher.objects.get(user=request.user)
    classes = ClassRoom.objects.all()
    if request.method == 'POST':
        from datetime import datetime
        in_time = request.POST.get('in_time')
        out_time = request.POST.get('out_time')
        fmt = '%H:%M'
        hours = 0
        if in_time and out_time:
            t1 = datetime.strptime(in_time, fmt)
            t2 = datetime.strptime(out_time, fmt)
            delta = t2 - t1
            hours = round(delta.total_seconds() / 3600, 2)
        WorkLog.objects.create(
            teacher=teacher,
            date=request.POST.get('date'),
            in_time=in_time,
            out_time=out_time,
            hours_worked=hours,
            class_room_id=request.POST.get('class_room'),
            subject=request.POST.get('subject'),
            syllabus_covered=request.POST.get('syllabus_covered'),
        )
        return redirect('teacher_worklog')
    return render(request, 'worklogApp/add_worklog.html', {'classes': classes})

@staff_member_required
def admin_worklog_list(request):
    from django.db.models import Sum
    from datetime import date
    worklogs = WorkLog.objects.select_related('teacher', 'class_room').all().order_by('-date')
    teacher_summary = []
    teachers = Teacher.objects.all()
    for teacher in teachers:
        logs = WorkLog.objects.filter(teacher=teacher)
        month_start = date.today().replace(day=1)
        monthly = logs.filter(date__gte=month_start)
        total_hours = monthly.aggregate(Sum('hours_worked'))['hours_worked__sum'] or 0
        amount = teacher.hourly_rate * total_hours if teacher.hourly_rate else 0
        teacher_summary.append({
            'teacher': teacher,
            'total_hours': total_hours,
            'total_days': monthly.count(),
            'amount': amount,
        })
    return render(request, 'worklogApp/admin_worklog_list.html', {'worklogs': worklogs, 'teacher_summary': teacher_summary})
