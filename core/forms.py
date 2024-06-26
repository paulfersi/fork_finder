from django import forms

from django import forms

class ReviewForm(forms.Form):
    place_search = forms.CharField(label="Search Place", widget=forms.TextInput(attrs={'id': 'id_place_search'}))
    place_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(widget=forms.HiddenInput(), required=False)
    location = forms.CharField(widget=forms.HiddenInput(), required=False)
    body = forms.CharField(widget=forms.Textarea, label="Review")
    rating = forms.IntegerField(label="Rating", min_value=1, max_value=5)
    photo = forms.ImageField(label="Photo", required=False)