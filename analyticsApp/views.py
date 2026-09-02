from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Avg, Count
from studentsApp.models import Student
from teachersApp.models import Teacher
from parentsApp.models import Parent
from feesApp.models import Fees
from resultsApp.models import Result
from attendanceApp.models import Attendance
from classesApp.models import ClassRoom
from accountsApp.models import Notice

@staff_member_required
def analytics_dashboard(request):
    total_students = Student.objects.count()
    total_teachers = Teacher.objects.count()
    total_parents = Parent.objects.count()
    total_classes = ClassRoom.objects.count()
    total_notices = Notice.objects.count()

    # Fees analytics
    total_fees = Fees.objects.aggregate(total=Sum('amount'))['total'] or 0
    paid_fees = Fees.objects.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
    pending_fees = Fees.objects.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0

    # Results analytics
    total_results = Result.objects.count()
    avg_percentage = Result.objects.aggregate(avg=Avg('marks'))['avg'] or 0

    # Attendance analytics
    total_attendance = Attendance.objects.count()
    present_count = Attendance.objects.filter(status='present').count()

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_parents': total_parents,
        'total_classes': total_classes,
        'total_notices': total_notices,
        'total_fees': total_fees,
        'paid_fees': paid_fees,
        'pending_fees': pending_fees,
        'total_results': total_results,
        'avg_percentage': avg_percentage,
        'total_attendance': total_attendance,
        'present_count': present_count,
    }
    return render(request, 'analyticsApp/dashboard.html', context)

from django.contrib.auth.decorators import login_required
from studentsApp.models import Student
from feesApp.models import Fees
from resultsApp.models import Result
from attendanceApp.models import Attendance

@login_required
def student_analytics(request):
    student = Student.objects.get(user=request.user)
    fees_list = Fees.objects.filter(student=student)
    course_fees = student.class_room.fees if student.class_room else 0
    paid_fees = sum(f.amount for f in fees_list if f.status == 'paid')
    pending_fees = max(course_fees - paid_fees, 0)
    total_fees = course_fees

    results = Result.objects.filter(student=student).select_related('exam')
    subject_names = [r.exam.subject for r in results]
    subject_marks = [float(r.marks) for r in results]
    avg_marks = sum(subject_marks) / len(subject_marks) if subject_marks else 0

    attendance = Attendance.objects.filter(student=student)
    total_attendance = attendance.count()
    present_count = attendance.filter(status='present').count()
    absent_count = attendance.filter(status='absent').count()
    late_count = attendance.filter(status='late').count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance else 0

    return render(request, 'analyticsApp/student_dashboard.html', {
        'student': student,
        'total_fees': total_fees,
        'paid_fees': paid_fees,
        'pending_fees': pending_fees,
        'avg_marks': avg_marks,
        'total_attendance': total_attendance,
        'present_count': present_count,
        'absent_count': absent_count,
        'late_count': late_count,
        'attendance_percentage': attendance_percentage,
        'subject_names': subject_names,
        'subject_marks': subject_marks,
    })
