# dwitter/admin.py

from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile,Review,Restaurant

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    # only username
    fields = ["username"]
    inlines = [ProfileInline]   #modify them in the same place

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Review)
admin.site.register(Restaurant)