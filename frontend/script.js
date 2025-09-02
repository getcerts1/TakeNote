const apiBase = '/api';

// ------------------- Signup -------------------
window.signup = async function() {
    const username = document.getElementById('signup-username').value;
    const password = document.getElementById('signup-password').value;

    const res = await fetch(`${apiBase}/signin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (data.message) {
        alert('Sign up successful. Please login.');
        window.location.href = '/login'; // redirect to login
    } else {
        alert(data.error || 'Sign up failed');
    }
}

// ------------------- Login -------------------
window.login = async function() {
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;

    const res = await fetch(`${apiBase}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await res.json();
    if (data.access_token) {
        localStorage.setItem('token', data.access_token);
        localStorage.setItem('username', username); // store username for display
        window.location.href = '/app';
    } else {
        alert(data.error || 'Login failed');
    }
}

// ------------------- Logout -------------------
window.logout = function() {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = '/';
}

// ------------------- Display Username -------------------
document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');

    if (window.location.pathname === '/app') { // only on app page
        if (!token || !username) {
            window.location.href = '/'; // redirect to login if not authenticated
            return;
        }
        document.getElementById('user-info').innerHTML = `<p>Welcome, <strong>${username}</strong></p>`;
    }
});

// ------------------- Create Note -------------------
window.createNote = async function() {
    const token = localStorage.getItem('token');
    const note_name = document.getElementById('note-name').value;
    const note_value = document.getElementById('note-value').value;
    const expiration = parseInt(document.getElementById('note-expiration').value);

    const res = await fetch(`${apiBase}/create`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ note_name, note_value, expiration })
    });

    const data = await res.json();
    const resultDiv = document.getElementById('note-result');
    if (data.message) {
        resultDiv.innerHTML = `<p style="color: green;">${data.message} (expires in ${data.expires_in} sec)</p>`;
    } else {
        resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
    }
}

// ------------------- Get Note -------------------
window.getNote = async function() {
    const token = localStorage.getItem('token');
    const name = document.getElementById('fetch-note-name').value;

    const res = await fetch(`${apiBase}/notes/${name}`, {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const data = await res.json();
    const resultDiv = document.getElementById('note-result');
    if (data.note_name) {
        resultDiv.innerHTML = `<p><strong>${data.note_name}:</strong> ${data.note_value} (expires in ${data.expires_in} sec)</p>`;
    } else {
        resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
    }
}
