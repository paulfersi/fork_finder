from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Review,Restaurant
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.views import View
from django.conf import settings
import json 

@login_required
def feed_view(request):
    return render(request, 'feed.html')

@login_required
def account_view(request):
    # logic to get account data
    return render(request, 'account.html')


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

def search_user_view(request):
    query = request.GET.get('q')
    if query:
        try:
            user = User.objects.get(username=query)
            return redirect('profile', pk=user.profile.pk)
        except User.DoesNotExist:
            return render(request, 'user_not_found.html', {'query': query})
    return redirect('feed')


class AddReviewView(View):
    def get(self, request):
        form = ReviewForm()
        return render(request, 'add_review.html', {
            'form': form,
            'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN
        })
    

def save_review(request):
    if request.method == "POST":
        data = json.loads(request.body)
        restaurant = Restaurant()
        restaurant.name = data['name']
        restaurant.location = data['location']