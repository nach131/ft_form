// Update progress bar based on form completion
function updateProgress() {
    const checkboxes = document.querySelectorAll('.form-check-input');
    let completed = 0;

    checkboxes.forEach((checkbox) => {
        if (checkbox.checked) {
            completed += parseInt(checkbox.value);
        }
    });

    const progressBar = document.getElementById('progressBar');
    progressBar.style.width = completed + '%';
    progressBar.setAttribute('aria-valuenow', completed);
    progressBar.textContent = completed + '%';
}

// Log out function
async function logout() {
    alert('Logging out...');

    const baseUrl = window.location.origin; 
    const url = `${baseUrl}/logout`;
    const cookies = document.cookie.split(';').map(cookie => cookie.trim());
    
    const data = {
        'sessionid': (cookies.find(cookie => cookie.startsWith('sessionid')) || '').split('=')[1] || '',
        'csrftoken': (cookies.find(cookie => cookie.startsWith('csrftoken')) || '').split('=')[1] || '',
        '_intra_42_session_production': (cookies.find(cookie => cookie.startsWith('_intra_42_session_production')) || '').split('=')[1] || '',
        'username': localStorage.getItem("username")
    };
    console.log('data', data);
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'include',
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log('Logout successful:', responseData);
    } catch (error) {
        console.error('There was a problem with the logout request:', error);
    }
    window.location.href = '/';
}