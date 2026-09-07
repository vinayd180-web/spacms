from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile

@login_required
def update_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profile_photo'):
            profile.profile_photo = request.FILES['profile_photo']

        profile.save()
        messages.success(request, "Profile updated!")
        return redirect('update_profile')
    return render(request, 'profileApp/update_profile.html', {'profile': profile})

@login_required
def my_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'profileApp/my_profile.html', {'profile': profile})
