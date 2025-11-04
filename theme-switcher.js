/**
 * @file This file handles the theme switching logic (dark/light mode) for the Event Horizon website.
 * @author Jules
 */

document.addEventListener('DOMContentLoaded', () => {
    const themeToggleButton = document.getElementById('theme-toggle');
    const themeToggleIcon = themeToggleButton.querySelector('span');

    // Appliquer le thème sauvegardé au chargement de la page
    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        themeToggleIcon.textContent = 'dark_mode';
    } else {
        document.documentElement.classList.remove('dark');
        themeToggleIcon.textContent = 'light_mode';
    }

    themeToggleButton.addEventListener('click', () => {
        // Basculer le thème
        const isDarkMode = document.documentElement.classList.toggle('dark');
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');

        // Mettre à jour l'icône
        themeToggleIcon.textContent = isDarkMode ? 'dark_mode' : 'light_mode';
    });

});
