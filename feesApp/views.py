from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Fees
from studentsApp.models import Student

UPI_ID = "shreeparthacademy2009-2@okaxis"
WHATSAPP_NUMBER = "919011395913"

@login_required
def student_fees(request):
    student = get_object_or_404(Student, user=request.user)
    fees_list = Fees.objects.filter(student=student).order_by('-due_date')
    total_fees = sum(fee.amount for fee in fees_list)
    paid_fees = sum(fee.amount for fee in fees_list if fee.status == 'paid')
    pending_fees = total_fees - paid_fees

    return render(request, 'feesApp/student_fees.html', {
        'fees_list': fees_list,
        'upi_id': UPI_ID,
        'whatsapp_number': WHATSAPP_NUMBER,
        'total_fees': total_fees,
        'paid_fees': paid_fees,
        'pending_fees': pending_fees,
    })

@login_required
def student_id_card(request):
    student = get_object_or_404(Student, user=request.user)
    return render(request, 'feesApp/student_id_card.html', {'student': student})

@staff_member_required
def admin_fees_list(request):
    fees_list = Fees.objects.select_related('student').all().order_by('status', 'student')
    return render(request, 'feesApp/admin_fees_list.html', {'fees_list': fees_list})

@staff_member_required
def admin_fees_update(request, fees_id):
    fee = get_object_or_404(Fees, id=fees_id)
    if request.method == 'POST':
        fee.status = request.POST.get('status')
        fee.transaction_id = request.POST.get('transaction_id', '')
        fee.save()
        return redirect('admin_fees_list')
    return render(request, 'feesApp/admin_fees_update.html', {'fee': fee})

@staff_member_required
def admin_student_id_cards(request):
    students = Student.objects.select_related('user').all().order_by('class_room', 'user__username')
    return render(request, 'feesApp/admin_student_id_cards.html', {'students': students})

@staff_member_required
def admin_student_id_card_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'feesApp/student_id_card.html', {'student': student})

def payment_gateway(request):
    return render(request, 'feesApp/payment_gateway.html')
