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
function logout() {
    alert('Logging out...');
    // Example: window.location.href = '/login.html';
}