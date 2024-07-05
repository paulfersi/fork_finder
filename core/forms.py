from django import forms
from .models import Review

class ReviewForm(forms.Form):
    review = forms.CharField(widget=forms.Textarea, label='Your Review')