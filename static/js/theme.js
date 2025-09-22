// Theme toggle functionality
document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('theme-switch');
    const themeLabel = document.querySelector('.theme-label');

    // Load saved theme immediately
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    if (themeSwitch && themeLabel) {
        themeSwitch.checked = savedTheme === 'dark';
        themeLabel.textContent = savedTheme === 'dark' ? '☀️' : '🌙';

        // Toggle theme
        themeSwitch.addEventListener('change', function() {
            const theme = this.checked ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
            themeLabel.textContent = theme === 'dark' ? '☀️' : '🌙';
        });
    }
});