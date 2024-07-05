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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core.views import UserCreateView, landing_page_view, pro_login_view
from django.conf.urls.static import static
from django.conf import settings
from .settings import MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('core.urls')),
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/",auth_views.LoginView.as_view(template_name='registration/login.html'), name="login"), 
    path("logout/",auth_views.LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
    path('',include('recommendations.urls')),
    path('', landing_page_view, name='landing_page'),
    path('pro-login/', pro_login_view, name='pro_login'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
