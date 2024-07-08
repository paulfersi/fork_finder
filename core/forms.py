from django import forms
from .models import Review, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User


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
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            Profile.objects.create(user=user, user_type='regular')
            group, created = Group.objects.get_or_create(name='Regular')
            group.user_set.add(user)
        return user

class CreateCriticUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        user = super().save(commit)
        if commit:
            profile = Profile.objects.create(user=user, user_type='critic')
            profile.save()
            group, created = Group.objects.get_or_create(name='Critics')
            group.user_set.add(user)
        return user