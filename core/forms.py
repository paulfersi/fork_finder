from django import forms
from .models import Review, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body', 'rating', 'photo']


class CriticReviewForm(forms.ModelForm):
    taste_rating = forms.IntegerField(label='Global Taste Rating', min_value=1, max_value=5, required=False)
    presentation_rating = forms.IntegerField(label='Presentation Rating', min_value=1, max_value=5, required=False)
    service_rating = forms.IntegerField(label='Service Rating', min_value=1, max_value=5, required=False)

    class Meta:
        model = Review
        fields = ['body', 'rating', 'photo', 'taste_rating', 'presentation_rating', 'service_rating', ]


class CreateRegularUser(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        profile, created = Profile.objects.get_or_create(user=user)
        profile.user_type = 'regular'
        profile.save()
        group, created = Group.objects.get_or_create(name="Regular")
        group.user_set.add(user)
        return user

class CreateCriticUser(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        profile, created = Profile.objects.get_or_create(user=user)
        if created:
            profile.user_type = 'critic'
            profile.save()
        group, created = Group.objects.get_or_create(name="Critics")
        group.user_set.add(user)
        content_type = ContentType.objects.get_for_model(Review)

        permission = Permission.objects.filter(
            codename='can_write_featured_review',
            content_type=content_type,
        ).first()

        if permission is None:
            permission = Permission.objects.create(
                codename='can_write_featured_review',
                name='Can write featured review',
                content_type=content_type,
            )

        if permission not in group.permissions.all():
            group.permissions.add(permission)
