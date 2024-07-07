from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
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
from .utils import get_recommended_reviews
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator

MAPBOX_TOKEN = settings.MAPBOX_ACCESS_TOKEN

@method_decorator(login_required, name='dispatch')
class FeedView(View):
    template_name = 'feed.html'

    def get(self, request, *args, **kwargs):
        recommended_reviews = get_recommended_reviews(request.user)
        profile = request.user.profile
        favorite_reviews = profile.favorite_reviews.all()
        return render(request, self.template_name, {
            "recommended_reviews": recommended_reviews,
            "favorite_reviews": favorite_reviews,
        })

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        favorite_reviews = profile.favorite_reviews.all()
        data = request.POST
        review_id = data.get("review_id")
        if review_id:
            review = get_object_or_404(Review, pk=review_id)
            if review in favorite_reviews:
                profile.favorite_reviews.remove(review)
            else:
                profile.favorite_reviews.add(review)
            profile.save()
            #update
            favorite_reviews = profile.favorite_reviews.all()

        recommended_reviews = get_recommended_reviews(request.user)
        return render(request, self.template_name, {
            "recommended_reviews": recommended_reviews,
            "favorite_reviews": favorite_reviews,
        })


@login_required
def account_view(request):
    return render(request, 'account.html')

def landing_page_view(request):
    return render(request, 'landing_page.html')

def pro_login_view(request):
    return render(request, 'registration/pro_login.html')

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
    return user.profile.user_type == 'critic'

def search_user_view(request):
    query = request.GET.get('q')
    if query:
        try:
            user = User.objects.get(username=query)
            return redirect('profile', pk=user.profile.pk)
        except User.DoesNotExist:
            return render(request, 'user_not_found.html', {'query': query})
    return redirect('feed')


@method_decorator(login_required, name='dispatch')
class AddReviewView(View):
    def get(self, request, *args, **kwargs):
        form = ReviewForm()
        mapbox_access_token = settings.MAPBOX_ACCESS_TOKEN
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

            # Check if the user has permission to mark a review as featured
            if request.user.profile.is_culinary_critic:
                review.is_featured = True
                review.taste_rating = form.cleaned_data['taste_rating']
                review.presentation_rating = form.cleaned_data['presentation_rating']
                review.service_rating = form.cleaned_data['service_rating']
            else:
                review.is_featured = False
            
            review.save()

            return redirect('feed')  

        
        return render(request, 'add_review.html', {'form': form, 'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN})
    
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


def view_on_map(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, pk=restaurant_id)
    return render(request, 'map.html', {'restaurant': restaurant, 'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN})