from django.urls import path
from .views import feed_view, account_view, save_review,profile_view,search_user_view, AddReviewView

urlpatterns = [
    path("", feed_view, name="feed"),
    path('account/', account_view, name='account'),
    path('add_review/', AddReviewView.as_view(), name='add_review'),
    path("profile/<int:pk>/", profile_view, name="profile"),
    path('search/', search_user_view, name='search_user'),
    path('save_review/',save_review,name  ='save_review')
]