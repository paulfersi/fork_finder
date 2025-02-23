from django.contrib import admin
from django.contrib.auth.models import User, Group,Permission
from .models import Profile,Review,Restaurant
from django.contrib.contenttypes.models import ContentType


class ProfileInline(admin.StackedInline):
    model = Profile
    fields = ["user","user_type","latitude","longitude","follows"]

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ["username", "password"]
    inlines = [ProfileInline]   #modify them in the same place



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Restaurant)