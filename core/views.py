from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile

@login_required
def feed_view(request):
    return render(request, 'feed.html')

@login_required
def account_view(request):
    # logic to get account data
    return render(request, 'account.html')

@login_required
def add_review_view(request):
    # logic to handle review submission
    return render(request, 'add_review.html')

def profile_list_view(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "profile_list.html", {"profiles": profiles})

def profile_view(request,pk):
    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "profile.html", {"profile": profile})
