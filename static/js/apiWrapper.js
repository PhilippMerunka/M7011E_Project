// apiWrapper.js
async function apiFetch(url, options = {}) {
    try {
        // Add the Authorization header with the access token
        const token = localStorage.getItem('accessToken');
        if (!options.headers) {
            options.headers = {};
        }
        options.headers['Authorization'] = `Bearer ${token}`;
        options.headers['Content-Type'] = 'application/json';

        // Make the API request
        const response = await fetch(url, options);

        // Check for 401 Unauthorized
        if (response.status === 401) {
            handleSessionExpiration();
            return response; // Still return the response if needed for debugging
        }

        if (response.status === 404) {
            handleNotFound();
            return response;
        }

        return response; // Return the response for other status codes
    } catch (error) {
        console.error('API Fetch Error:', error);
        alert('An unexpected error occurred. Please try again later.');
        throw error; // Re-throw the error for further handling
    }
}

// Handle session expiration
function handleSessionExpiration() {
    alert('Your session has expired. Please log in again.');
    // Clear tokens from local storage
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    // Redirect to the login page
    window.location.href = '/users/login/';
}

// Handle 404 errors
function handleNotFound() {
    const token = localStorage.getItem('accessToken');

    if (!token) {
        // If no token is available, redirect to the login page
        alert('Page not found. Please log in.');
        window.location.href = '/users/login/';
    } else {
        // If a token is available, redirect to the products page
        alert('Page not found. Redirecting to the products page.');
        window.location.href = '/products/';
    }
}