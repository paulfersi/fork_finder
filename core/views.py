from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile,Review,Restaurant
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.views import View
from django.urls import reverse_lazy
import json
from django.conf import settings
from django.contrib import messages

MAPBOX_TOKEN = settings.MAPBOX_ACCESS_TOKEN

@login_required
def feed_view(request):
    return render(request, 'feed.html')

@login_required
def account_view(request):
    # logic to get account data
    return render(request, 'account.html')

class UserCreateView(CreateView): 
    form_class = UserCreationForm 
    template_name = "registration/user_create.html" 
    success_url = reverse_lazy("login")

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

def is_critic(user):
    return user.userprofile.user_type == 'critic'

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
    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        mapbox_access_token = settings.MAPBOX_ACCESS_TOKEN  # Replace with your actual Mapbox access token
        return render(request, 'add_review.html', {'form': form, 'mapbox_access_token': mapbox_access_token})

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            selected_place = json.loads(request.POST.get('selected_place', '{}'))
            place_id = selected_place.get('place_id')
            name = selected_place.get('name')
            address = selected_place.get('address')
            latitude = selected_place.get('latitude')
            longitude = selected_place.get('longitude')

            
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={
                    'name': name,
                    'address': address,
                    'latitude': latitude,
                    'longitude': longitude,
                }
            )

            review = form.save(commit=False)
            review.user = request.user  
            review.restaurant = restaurant
            review.save()

            return redirect('feed')  # Redirect to your feed or any other view upon successful submission

        # If form is invalid, render the form again with errors
        mapbox_access_token = 'YOUR_MAPBOX_ACCESS_TOKEN'  # Replace with your actual Mapbox access token
        return render(request, 'add_review.html', {'form': form, 'mapbox_access_token': mapbox_access_token})


@login_required
def edit_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=request.user.pk)
    else:
        form = ReviewForm(instance=review)
    
    return render(request, 'edit_review.html', {'form': form, 'review': review})

@login_required
def delete_review(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully.')
        return redirect('profile', pk=request.user.profile.pk)

    return redirect('profile', pk=request.user.pk)