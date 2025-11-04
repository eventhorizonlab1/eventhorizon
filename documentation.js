/**
 * @file Central repository for all documented JavaScript functions,
 * including animations and theme switching.
 * @author Jules
 */

/**
 * Initializes all animations and event listeners when the DOM is fully loaded.
 */
function initializeWebsiteInteractivity() {
    // Animation functions
    animateMainTitle();
    animateMenuItems();
    setupIntersectionObserver();
    setupQuickLinkHovers();
    setupThemeToggleGlow();

    // Theme switcher functions
    initializeTheme();
    setupThemeToggleListener();
}

/**
 * Animates the main title on page load.
 * The title fades in and slides down.
 */
function animateMainTitle() {
    anime({
        targets: '.main-title',
        opacity: [0, 1],
        translateY: [-50, 0],
        duration: 1000,
        ease: 'easeOutExpo'
    });
}

/**
 * Animates the menu items on page load.
 * Each item fades in and slides from the left with a staggered delay.
 */
function animateMenuItems() {
    anime({
        targets: '.menu-item',
        opacity: [0, 1],
        translateX: [-50, 0],
        duration: 800,
        delay: anime.stagger(100),
        ease: 'easeOutExpo'
    });
}

/**
 * Sets up an Intersection Observer to animate sections as they enter the viewport.
 * Sections fade in and slide up when they become visible.
 */
function setupIntersectionObserver() {
    const sections = document.querySelectorAll('.animate-section');
    if (sections.length === 0) return;

    // Initially hide the sections
    anime.set(sections, {
        opacity: 0,
        translateY: 50
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                anime({
                    targets: entry.target,
                    opacity: 1,
                    translateY: 0,
                    duration: 1000,
                    ease: 'easeOutExpo'
                });
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1
    });

    sections.forEach(section => {
        observer.observe(section);
    });
}

/**
 * Sets up hover effects for the quick links in the footer.
 * Links move up and change color on hover.
 */
function setupQuickLinkHovers() {
    const quickLinks = document.querySelectorAll('.quick-link');
    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            anime({
                targets: link,
                translateY: -5,
                color: '#06ccf9',
                duration: 300,
                ease: 'easeOutExpo'
            });
        });

        link.addEventListener('mouseleave', () => {
            const isDarkMode = document.documentElement.classList.contains('dark');
            anime({
                targets: link,
                translateY: 0,
                color: isDarkMode ? 'rgba(255, 255, 255, 0.6)' : 'rgba(0, 0, 0, 0.6)',
                duration: 300,
                ease: 'easeOutExpo'
            });
        });
    });
}

/**
 * Adds a "glow" effect to the theme toggle button on hover.
 */
function setupThemeToggleGlow() {
    const themeToggleButton = document.getElementById('theme-toggle');
    if (themeToggleButton) {
        themeToggleButton.addEventListener('mouseenter', () => {
            anime({
                targets: themeToggleButton,
                boxShadow: '0 0 12px #06ccf9',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });

        themeToggleButton.addEventListener('mouseleave', () => {
            anime({
                targets: themeToggleButton,
                boxShadow: '0 0 0 rgba(0,0,0,0)',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
    }
}

/**
 * Initializes the theme based on localStorage or user's system preference.
 */
function initializeTheme() {
    const themeToggleButton = document.getElementById('theme-toggle');
    if (!themeToggleButton) return;
    const themeToggleIcon = themeToggleButton.querySelector('span');

    if (localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark');
        themeToggleIcon.textContent = 'dark_mode';
    } else {
        document.documentElement.classList.remove('dark');
        themeToggleIcon.textContent = 'light_mode';
    }
}

/**
 * Animates the theme transition with a fade and zoom effect.
 */
function animateAndToggleTheme() {
    const isDarkMode = document.documentElement.classList.contains('dark');

    const timeline = anime.timeline({
        duration: 400, // Each phase of the animation will be 0.4s, total 0.8s
        easing: 'easeInOutExpo'
    });

    timeline
        .add({
            targets: 'body',
            opacity: [1, 0],
            scale: [1, 0.98],
            complete: () => {
                const themeToggleButton = document.getElementById('theme-toggle');
                const themeToggleIcon = themeToggleButton.querySelector('span');
                document.documentElement.classList.toggle('dark');
                const newIsDarkMode = document.documentElement.classList.contains('dark');
                localStorage.setItem('theme', newIsDarkMode ? 'dark' : 'light');
                themeToggleIcon.textContent = newIsDarkMode ? 'dark_mode' : 'light_mode';
            }
        })
        .add({
            targets: 'body',
            opacity: [0, 1],
            scale: [0.98, 1]
        });
}

/**
 * Sets up the event listener for the theme toggle button.
 * Toggles the theme and updates the icon on click.
 */
function setupThemeToggleListener() {
    const themeToggleButton = document.getElementById('theme-toggle');
    if (!themeToggleButton) return;

    themeToggleButton.addEventListener('click', () => {
        animateAndToggleTheme();
    });
}

// Initialize everything after the DOM is loaded.
document.addEventListener('DOMContentLoaded', initializeWebsiteInteractivity);
