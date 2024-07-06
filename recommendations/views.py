# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from core.models import Profile

@login_required
@csrf_protect
def get_location(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        profile = Profile.objects.get(user=request.user)
        profile.latitude = latitude
        profile.longitude = longitude
        profile.save()
        return redirect('feed')
    return render(request, 'get_location.html')
