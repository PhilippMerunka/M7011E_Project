const tokenManager = {
    getAccessToken: async () => {
        const accessToken = localStorage.getItem('accessToken');
        const refreshToken = localStorage.getItem('refreshToken');

        if (accessToken && !isTokenExpired(accessToken)) {
            return accessToken;
        } else if (refreshToken) {
            return await tokenManager.refreshAccessToken(refreshToken);
        } else {
            // Redirect to login if no valid tokens
            window.location.href = '/users/login/';
        }
    },

    refreshAccessToken: async () => {
        const refreshToken = localStorage.getItem('refreshToken');

        if (!refreshToken) {
            alert('Session expired. Please log in again.');
            localStorage.clear();
            window.location.href = '/users/login/';
            return;
        }

        try {
            const response = await fetch('/api/users/token/refresh/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: refreshToken }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access);
                if (data.refresh) {
                    localStorage.setItem('refreshToken', data.refresh);
                }
                return data.access;
            } else {
                console.error('Failed to refresh token:', await response.text());
                alert('Session expired. Please log in again.');
                localStorage.clear();
                window.location.href = '/users/login/';
            }
        } catch (error) {
            console.error('Error refreshing token:', error);
            alert('An error occurred. Please log in again.');
            localStorage.clear();
            window.location.href = '/users/login/';
        }
    },
};

function isTokenExpired(token) {
    const payload = JSON.parse(atob(token.split('.')[1])); // Decode JWT payload
    return payload.exp * 1000 < Date.now();
}
