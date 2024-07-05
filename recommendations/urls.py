from django.urls import path
from .views import get_location

urlpatterns = [
    path('get_location/', get_location, name='get_location'),
]