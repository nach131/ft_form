const darkModeIcon = document.getElementById('darkModeIcon');
const lightModeIcon = document.getElementById('lightModeIcon');

const switchTheme = () => {
    const body = document.body;

    if (body.classList.contains('dark-theme')) {
        // Switch to light theme
        body.classList.remove('dark-theme');
        body.classList.add('light-theme');
        lightModeIcon.classList.remove('d-none');
        darkModeIcon.classList.add('d-none');
    } else {
        // Switch to dark theme
        body.classList.remove('light-theme');
        body.classList.add('dark-theme');
        darkModeIcon.classList.remove('d-none');
        lightModeIcon.classList.add('d-none');
    }
};

// Event listeners for theme icons
darkModeIcon.addEventListener('click', switchTheme);
lightModeIcon.addEventListener('click', switchTheme);