from django import forms
from .models import Review, Restaurant

class ReviewForm(forms.ModelForm):
    place_search = forms.CharField(label="Search for a place", max_length=255, required=True)
    place_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    
    class Meta:
        model = Review
        fields = ['body', 'rating', 'photo']

    def save(self, commit=True):
        place_id = self.cleaned_data.get('place_id')
        # Fetch the place details using Google Maps API if the restaurant does not already exist
        restaurant, created = Restaurant.objects.get_or_create(place_id=place_id, defaults={
            'name': self.cleaned_data['place_search'],
            'location': 'Location Placeholder'  # Update this with actual location if needed
        })
        self.instance.restaurant = restaurant
        return super().save(commit)
