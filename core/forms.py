from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    taste_rating = forms.IntegerField(label='Global Taste Rating', min_value=1, max_value=5, required=False)
    presentation_rating = forms.IntegerField(label='Presentation Rating', min_value=1, max_value=5, required=False)
    service_rating = forms.IntegerField(label='Service Rating', min_value=1, max_value=5, required=False)

    class Meta:
        model = Review
        fields = ['body', 'rating', 'photo', 'taste_rating', 'presentation_rating', 'service_rating']

