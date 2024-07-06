from django.urls import path
from .views import feed_view, account_view,profile_view,search_user_view, AddReviewView, edit_review, delete_review

STATIC_URL = "/media/static"

urlpatterns = [
    path('feed/', feed_view, name="feed"),
    path('account/', account_view, name='account'),
    path('add_review/', AddReviewView.as_view(), name='add_review'),
    path("profile/<int:pk>/", profile_view, name="profile"),
    path('search/', search_user_view, name='search_user'),
    path('edit_review/<int:pk>/', edit_review, name='edit_review'),
    path('review/delete/<int:pk>/', delete_review, name='delete_review'),
] 