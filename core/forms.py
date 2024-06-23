from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['restaurant', 'body', 'rating', 'photo']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'maxlength': 140}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
        labels = {
            'body': 'Review Text',
            'rating': 'Rating (1 to 5)',
            'photo': 'Upload Photo',
        }

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating