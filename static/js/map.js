document.addEventListener('DOMContentLoaded', function() {
    mapboxgl.accessToken = mapbox_access_token;
    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: [restaurant_longitude, restaurant_latitude],
        zoom: 15
    });

    new mapboxgl.Marker()
        .setLngLat([restaurant_longitude, restaurant_latitude])
        .setPopup(new mapboxgl.Popup().setHTML('<h3>' + restaurant_name + '</h3><p>' + restaurant_address + '</p>'))
        .addTo(map);
});
