from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event

@staff_member_required
def create_event(request):
    if request.method == 'POST':
        Event.objects.create(
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            event_date=request.POST.get('event_date'),
            start_time=request.POST.get('start_time'),
            end_time=request.POST.get('end_time'),
            venue=request.POST.get('venue'),
            created_by=request.user,
        )
        return redirect('event_list')
    return render(request, 'eventApp/create_event.html')

@login_required
def event_list(request):
    events = Event.objects.all().order_by('event_date')
    return render(request, 'eventApp/event_list.html', {'events': events})
