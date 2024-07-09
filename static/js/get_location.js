$(document).ready(function() {
    $('#locationModal').modal('show');
    
    // Handle modal close event
    $('#locationModal').on('hidden.bs.modal', function () {
        window.location.href = locationFeedUrl; // Set this variable dynamically in the template
    });
});

// handle getting location
document.getElementById('get-location-btn').onclick = function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            document.getElementById('latitude').value = position.coords.latitude;
            document.getElementById('longitude').value = position.coords.longitude;
            document.getElementById('location-form').style.display = 'block';
            $('#locationModal').modal('hide'); // Hide modal after getting location
            document.getElementById('location-form').submit(); // Submit the form
        }, function(error) {
            alert('Error getting location: ' + error.message);
        });
    } else {
        alert('Geolocation is not supported by this browser.');
    }
};

// handle refusing location
document.getElementById('refuse-location-btn').onclick = function() {
    document.getElementById('latitude').value = 44.647129; // Default latitude (Modena)
    document.getElementById('longitude').value = 10.925227; // Default longitude (Modena)
    document.getElementById('location-form').style.display = 'block';
    $('#locationModal').modal('hide'); // Hide modal after setting default location
    document.getElementById('location-form').submit(); // Submit the form
};
