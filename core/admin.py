from django.contrib import admin
from django.contrib.auth.models import User, Group,Permission
from .models import Profile,Review,Restaurant
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Review)
permission, created_permission = Permission.objects.get_or_create(
    codename='can_write_featured_review',
    name='Can write featured reviews',
    content_type=content_type
)

group1, created_group1 = Group.objects.get_or_create(name='Critics')
user = User.objects.get(username="admin")
user.groups.add(group1)
group1.permissions.add(permission)

group2, created_group2 = Group.objects.get_or_create(name='Regular')


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