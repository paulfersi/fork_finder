from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
