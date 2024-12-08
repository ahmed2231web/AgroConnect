const API_URL = 'http://127.0.0.1:8000';

// Registration functionality
async function register() {
    const email = document.getElementById('reg-email').value.trim();
    const fullName = document.getElementById('reg-fullName').value.trim();
    const phoneNumber = document.getElementById('reg-phone').value.trim();
    const cnic = document.getElementById('reg-cnic').value.trim();
    const user_type = document.getElementById('reg-userType').value;
    const password = document.getElementById('reg-password').value;
    const confirmPassword = document.getElementById('reg-confirm-password').value;

    // Basic validation
    if (!email || !fullName || !phoneNumber || !cnic || !password || !confirmPassword) {
        alert('Please fill in all fields');
        return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert('Please enter a valid email address');
        return;
    }

    // Password match validation
    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Password strength validation
    if (password.length < 8) {
        alert('Password must be at least 8 characters long');
        return;
    }

    // Phone number validation
    const phoneRegex = /^\+?[1-9]\d{9,14}$/;
    if (!phoneRegex.test(phoneNumber)) {
        alert('Please enter a valid phone number (e.g., +923001234567)');
        return;
    }

    // CNIC validation (13 digits)
    const cnicRegex = /^\d{13}$/;
    if (!cnicRegex.test(cnic)) {
        alert('Please enter a valid 13-digit CNIC number');
        return;
    }

    const userData = {
        email: email,
        fullName: fullName,
        phoneNumber: phoneNumber,
        cnic: cnic,
        user_type: user_type,
        password: password,
        re_password: confirmPassword
    };

    try {
        const response = await fetch(`${API_URL}/auth/users/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });

        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            window.location.href = 'login.html';
        } else {
            let errorMessage = 'Registration failed:\\n';
            if (typeof data === 'object') {
                Object.keys(data).forEach(key => {
                    if (Array.isArray(data[key])) {
                        errorMessage += `${key}: ${data[key].join(', ')}\\n`;
                    } else {
                        errorMessage += `${key}: ${data[key]}\\n`;
                    }
                });
            } else {
                errorMessage += data;
            }
            alert(errorMessage);
            console.error('Registration error:', data);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during registration. Please try again.');
    }
}

// Login functionality
async function login() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;

    if (!email || !password) {
        alert('Please enter both email and password');
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/jwt/create/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await response.json();
        
        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            window.location.href = 'home.html';
        } else {
            alert('Login failed: ' + (data.detail || 'Invalid credentials'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

// Home page functionality
async function loadUserInfo() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    try {
        const response = await fetch(`${API_URL}/auth/users/me/`, {
            headers: {
                'Authorization': `JWT ${token}`
            }
        });

        const data = await response.json();
        
        if (response.ok) {
            document.getElementById('user-name').textContent = data.fullName;
        } else {
            if (response.status === 401) {
                // Token expired or invalid
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = 'login.html';
            } else {
                alert('Failed to load user information');
            }
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while loading user information');
    }
}

// Logout functionality
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    window.location.href = 'login.html';
}

// Page load handlers
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the home page
    if (document.getElementById('user-name')) {
        loadUserInfo();
    }
    
    // Check if user is already logged in on login/register pages
    if (window.location.href.includes('login.html') || 
        window.location.href.includes('register.html')) {
        if (localStorage.getItem('access_token')) {
            window.location.href = 'home.html';
        }
    }
});