const script = document.getElementById('search-js');
script.onload = function () {
    const searchBox = document.querySelector('mapbox-search-box')

    // add an event listener to handle the `retrieve` event
    searchBox.addEventListener('retrieve', (e) => {
        const feature = e.detail;
        console.log(feature) // geojson object representing the selected item
    });
}


