from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Result
from studentsApp.models import Student
from examsApp.models import Exam

@login_required
def student_results(request):
    student = get_object_or_404(Student, user=request.user)
    results = Result.objects.filter(student=student).select_related('exam').order_by('exam__exam_date')
    return render(request, 'resultsApp/student_results.html', {'results': results})

@staff_member_required
def admin_results_list(request):
    results = Result.objects.select_related('student', 'exam').all().order_by('exam', 'student')
    return render(request, 'resultsApp/admin_results_list.html', {'results': results})

@staff_member_required
def admin_add_result(request):
    if request.method == 'POST':
        student_id = request.POST.get('student')
        exam_id = request.POST.get('exam')
        marks = request.POST.get('marks')
        grade = request.POST.get('grade', '')
        remarks = request.POST.get('remarks', '')
        student = get_object_or_404(Student, id=student_id)
        exam = get_object_or_404(Exam, id=exam_id)
        Result.objects.update_or_create(
            student=student, exam=exam,
            defaults={'marks': marks, 'grade': grade, 'remarks': remarks}
        )
        return redirect('admin_results_list')
    students = Student.objects.all()
    exams = Exam.objects.all()
    return render(request, 'resultsApp/admin_add_result.html', {'students': students, 'exams': exams})

@staff_member_required
def admin_update_result(request, result_id):
    result = get_object_or_404(Result, id=result_id)
    if request.method == 'POST':
        result.marks = request.POST.get('marks')
        result.grade = request.POST.get('grade', '')
        result.remarks = request.POST.get('remarks', '')
        result.save()
        return redirect('admin_results_list')
    return render(request, 'resultsApp/admin_update_result.html', {'result': result})

@login_required
def report_card(request):
    student = get_object_or_404(Student, user=request.user)
    results = Result.objects.filter(student=student).select_related('exam')
    total_marks = sum(r.marks for r in results)
    max_marks = sum(r.exam.max_marks for r in results if r.exam.max_marks)
    percentage = (total_marks / max_marks * 100) if max_marks else 0
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"
    return render(request, 'resultsApp/report_card.html', {
        'student': student,
        'results': results,
        'total_marks': total_marks,
        'max_marks': max_marks,
        'percentage': percentage,
        'grade': grade,
    })
