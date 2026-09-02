from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Complaint

@login_required
def file_complaint(request):
    if request.method == 'POST':
        Complaint.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            filed_by=request.user,
        )
        messages.success(request, "Complaint filed successfully!")
        return redirect('my_complaints')
    return render(request, 'complaintApp/file_complaint.html')

@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(filed_by=request.user)
    return render(request, 'complaintApp/my_complaints.html', {'complaints': complaints})

@staff_member_required
def all_complaints(request):
    complaints = Complaint.objects.select_related('filed_by').all()
    return render(request, 'complaintApp/all_complaints.html', {'complaints': complaints})

@staff_member_required
def resolve_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    if request.method == 'POST':
        complaint.status = request.POST.get('status')
        complaint.admin_response = request.POST.get('admin_response')
        complaint.save()
        messages.success(request, "Complaint updated!")
        return redirect('all_complaints')
    return render(request, 'complaintApp/resolve_complaint.html', {'complaint': complaint})
