from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'body', 'rating', 'photo']
        widgets = {
            'restaurant': forms.HiddenInput()
        }
