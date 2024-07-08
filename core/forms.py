from django import forms
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


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
        g = Group.objects.get(name="Regular") 
        g.user_set.add(user)
        return user
    
class CreateCriticUser(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        user.profile.user_type = 'Critic'
        g = Group.objects.get(name="Critic") 
        g.user_set.add(user)
        return user
    
