document.getElementById('logout-link').addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default link navigation
    document.getElementById('logout-form').submit(); // Submit the hidden form with POST
});