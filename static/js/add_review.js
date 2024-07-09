document.addEventListener('DOMContentLoaded', function() {
    mapboxgl.accessToken = mapbox_access_token;
    let map, marker;

    function searchRestaurant() {
        const restaurantName = document.getElementById('restaurant-name').value.trim();
        if (!restaurantName) {
            alert('Please enter a restaurant name.');
            return;
        }

        const bboxEurope = '-23.958156,31.052934,44.830131,71.185989';

        fetch(`https://api.mapbox.com/geocoding/v5/mapbox.places/${restaurantName}.json?access_token=${mapbox_access_token}&bbox=${bboxEurope}`)
            .then(response => response.json())
            .then(data => {
                const features = data.features.slice(0, 3); // Get first 3 suggestions

                if (features.length === 0) {
                    alert('No restaurant found. Please try again.');
                    return;
                }

                const suggestionsList = document.getElementById('suggestions-list');
                suggestionsList.innerHTML = ''; // Clear previous suggestions

                features.forEach((feature, index) => {
                    const suggestedRestaurant = {
                        place_id: feature.id,
                        name: feature.text,
                        latitude: feature.center[1],
                        longitude: feature.center[0],
                    };

                    if (feature.properties.address) {
                        suggestedRestaurant.address = feature.properties.address;
                    }

                    const suggestionItem = document.createElement('div');
                    suggestionItem.classList.add('list-group-item', 'list-group-item-action');
                    suggestionItem.innerHTML = `
                        <input type="radio" id="suggestion-${index}" name="selected_place" value='${JSON.stringify(suggestedRestaurant)}' ${index === 0 ? 'checked' : ''}>
                        <label for="suggestion-${index}" class="ml-2">${suggestedRestaurant.name}, ${suggestedRestaurant.address}</label>
                    `;
                    suggestionsList.appendChild(suggestionItem);

                    if (index === 0) {
                        displayMap(suggestedRestaurant.latitude, suggestedRestaurant.longitude);
                    }

                    suggestionItem.querySelector('input').addEventListener('change', function () {
                        displayMap(suggestedRestaurant.latitude, suggestedRestaurant.longitude);
                    });
                });

                document.getElementById('restaurant-suggestions').style.display = 'block';
                document.getElementById('submit-button').style.display = 'block';
            })
            .catch(error => {
                console.error('Error fetching restaurant suggestions:', error);
                alert('Error fetching restaurant suggestions. Please try again later.');
            });
    }

    function displayMap(latitude, longitude) {
        if (!map) {
            map = new mapboxgl.Map({
                container: 'map',
                style: 'mapbox://styles/mapbox/streets-v11',
                center: [longitude, latitude],
                zoom: 15
            });

            marker = new mapboxgl.Marker()
                .setLngLat([longitude, latitude])
                .addTo(map);
        } else {
            map.setCenter([longitude, latitude]);
            marker.setLngLat([longitude, latitude]);
        }
    }

    document.getElementById('search-button').addEventListener('click', searchRestaurant);
});
