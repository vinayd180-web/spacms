from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from studentsApp.models import Student
from teachersApp.models import Teacher
from parentsApp.models import Parent

@staff_member_required
def broadcast(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        platform = request.POST.get('platform')
        target = request.POST.get('target')

        contacts = []
        if target == 'students':
            students = Student.objects.select_related('user')
            contacts = [s.user for s in students]
        elif target == 'teachers':
            teachers = Teacher.objects.select_related('user')
            contacts = [t.user for t in teachers]
        elif target == 'parents':
            parents = Parent.objects.select_related('user')
            contacts = [p.user for p in parents]
        elif target == 'all':
            from accountsApp.models import User
            contacts = User.objects.all()

        if platform == 'whatsapp':
            whatsapp_link = f"https://wa.me/919011395913?text={message}"
            messages.success(request, f"WhatsApp broadcast prepared for {len(contacts)} users!")
            return render(request, 'communicationApp/broadcast.html', {'whatsapp_link': whatsapp_link})
        elif platform == 'telegram':
            telegram_link = f"https://t.me/ShreeParthAcademy?text={message}"
            messages.success(request, f"Telegram broadcast prepared for {len(contacts)} users!")
            return render(request, 'communicationApp/broadcast.html', {'telegram_link': telegram_link})

    return render(request, 'communicationApp/broadcast.html')
