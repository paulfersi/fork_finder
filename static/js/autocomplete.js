let autocomplete;

function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_place_search'),
        { types: ['restaurant'] }
    );
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    const place = autocomplete.getPlace();
    if (!place.place_id) {
        alert('Please select a restaurant from the suggestions.');
        return;
    }
    document.getElementById('id_place_id').value = place.place_id;
}

document.addEventListener('DOMContentLoaded', function() {
    loadGoogleMapsScript('initAutocomplete');
});
