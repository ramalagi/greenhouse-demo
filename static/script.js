// Auto-refresh soil data every 5 seconds
function updateSoilData() {
    fetch('/api/soil')
        .then(response => response.json())
        .then(data => {
            document.getElementById('moisture-bar').style.width = data.moisture + '%';
            document.getElementById('moisture-bar').textContent = data.moisture + '%';

            const tempPercent = (data.temperature / 50) * 100;
            document.getElementById('temperature-bar').style.width = tempPercent + '%';
            document.getElementById('temperature-bar').textContent = data.temperature + '°C';

            document.getElementById('humidity-bar').style.width = data.humidity + '%';
            document.getElementById('humidity-bar').textContent = data.humidity + '%';
        })
        .catch(error => console.error('Error updating soil data:', error));
}

// Update soil data on page load and every 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    updateSoilData();
    setInterval(updateSoilData, 5000);
});