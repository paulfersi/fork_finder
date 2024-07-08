from django.urls import path
from .views import FeedView,profile_view,search_user_view, AddReviewView, edit_review, delete_review, get_location,view_on_map,AddProReviewView

STATIC_URL = "/media/static"

urlpatterns = [
    path('feed/', FeedView.as_view(), name="feed"),
    path('add_review/', AddReviewView.as_view(), name='add_review'),
    path('add_pro_review/', AddProReviewView.as_view(), name='add_pro_review'),
    path("profile/<int:pk>/", profile_view, name="profile"),
    path('search/', search_user_view, name='search_user'),
    path('edit_review/<int:pk>/', edit_review, name='edit_review'),
    path('review/delete/<int:pk>/', delete_review, name='delete_review'),
    path('get_location/', get_location, name='get_location'),
    path('view_on_map/<int:restaurant_id>/', view_on_map, name='view_on_map'),
] 