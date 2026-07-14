// script.js - Client-side JavaScript for the web server

// Update time every second
function updateTime() {
    fetch('/api/time')
        .then(response => response.json())
        .then(data => {
            const timeElement = document.getElementById('time');
            if (timeElement) {
                const date = new Date(data.time);
                timeElement.textContent = date.toLocaleString();
            }
        })
        .catch(error => {
            console.error('Error fetching time:', error);
            const timeElement = document.getElementById('time');
            if (timeElement) {
                timeElement.textContent = 'Error loading time';
            }
        });
}

// Check server status
function checkStatus() {
    fetch('/api/info')
        .then(response => response.json())
        .then(data => {
            const statusElement = document.getElementById('status');
            if (statusElement) {
                statusElement.textContent = 'Online';
                statusElement.className = 'value';
            }
        })
        .catch(error => {
            console.error('Error checking status:', error);
            const statusElement = document.getElementById('status');
            if (statusElement) {
                statusElement.textContent = 'Offline';
                statusElement.className = 'value offline';
            }
        });
}

// Log API calls
function logAPICall(endpoint) {
    console.log(`[API] Called: ${endpoint} at ${new Date().toISOString()}`);
}

// Add click listeners to API links
document.addEventListener('DOMContentLoaded', function() {
    // Initial updates
    updateTime();
    checkStatus();
    
    // Update time every second
    setInterval(updateTime, 1000);
    
    // Log API link clicks
    document.querySelectorAll('.api-list a').forEach(link => {
        link.addEventListener('click', function(e) {
            logAPICall(this.getAttribute('href'));
        });
    });
    
    console.log('Client-side JavaScript loaded successfully!');
});

// Handle offline/online events
window.addEventListener('online', function() {
    console.log('Network connection restored');
    checkStatus();
});

window.addEventListener('offline', function() {
    console.log('Network connection lost');
    const statusElement = document.getElementById('status');
    if (statusElement) {
        statusElement.textContent = 'Offline';
        statusElement.className = 'value offline';
    }
});

console.log('Welcome to Python Web Server!');
console.log('Check the console for API call logs.');
