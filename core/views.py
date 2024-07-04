from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile,Review,Restaurant
from .forms import ReviewForm
from django.contrib.auth.models import User
from django.views import View

@login_required
def feed_view(request):
    return render(request, 'feed.html')

@login_required
def account_view(request):
    # logic to get account data
    return render(request, 'account.html')

@login_required
def add_review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            place_id = form.cleaned_data['place_id']
            name = form.cleaned_data['name']
            location = form.cleaned_data['location']

            # Check if the restaurant already exists
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={
                    'name': name,
                    'location': location,
                }
            )

            # Save the review
            review = Review(
                user=request.user,  # Assuming you have a logged-in user
                restaurant=restaurant,
                body=form.cleaned_data['body'],
                rating=form.cleaned_data['rating'],
                photo=form.cleaned_data.get('photo')
            )
            review.save()
            
            return redirect('feed')  # Redirect to a success page
    else:
        form = ReviewForm()

    return render(request, 'add_review.html', {'form': form})

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
        return render(request, 'add_review.html', {'form': form})

    def post(self, request):
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            place_id = request.POST.get('place_id')
            name = request.POST.get('name')
            location = request.POST.get('location')
            
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={'name': name, 'location': location}
            )
            review.restaurant = restaurant
            review.save()
            return redirect('feed')  
        return render(request, 'add_review.html', {'form': form})
