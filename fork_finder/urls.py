"""
URL configuration for fork_finder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import feed_view, account_view, add_review_view,profile_list_view

urlpatterns = [
    path("", feed_view, name="feed"),
    path("admin/", admin.site.urls),
    path('account/', account_view, name='account'),
    path('add_review/', add_review_view, name='add_review'),
    path("profile_list/", profile_list_view, name="profile_list"),

]
