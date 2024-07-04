function initializeMapboxAutocomplete(accessToken) {
    mapboxgl.accessToken = accessToken;
    var geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        types: 'poi',
        placeholder: 'Search for places'
    });

    geocoder.addTo('#place-input');

    geocoder.on('result', function(e) {
        document.getElementById('place-id').value = e.result.id;
        document.getElementById('place-name').value = e.result.text;
        document.getElementById('place-location').value = e.result.place_name;
    });
}

document.addEventListener("DOMContentLoaded", function() {
    initializeMapboxAutocomplete(mapboxAccessToken);
});
