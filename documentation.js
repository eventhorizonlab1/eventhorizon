/**
 * @file Central repository for all documented JavaScript functions,
 * including animations, theme switching, and other interactive features.
 * This file is fully documented with JSDoc.
 * @author Jules
 */

/**
 * Initializes all animations and event listeners when the DOM is fully loaded.
 * It serves as the main entry point for all client-side interactivity.
 *
 * @returns {void} This function does not return a value.
 */
function initializeWebsiteInteractivity() {
    const timeline = anime.timeline({
        easing: 'easeOutExpo',
        duration: 1000
    });

    timeline
        .add(animateHeader())
        .add(animateMainTitle(), '-=500');

    setupIntersectionObserver();
    setupQuickLinkHovers();
    setupLogoHoverAnimation();
}

/**
 * Animates the main title on page load.
 * The title fades in and slides down for a smooth entrance effect.
 *
 * @returns {void} This function does not return a value.
 */
function animateMainTitle() {
    const mainTitle = document.querySelector('.main-title');
    if (!mainTitle) return;

    const words = mainTitle.innerText.split(' ');
    mainTitle.innerHTML = words.map(word => `<span>${word}</span>`).join(' ');

    return anime({
        targets: '.main-title span',
        opacity: [0, 1],
        translateY: [50, 0],
        delay: anime.stagger(100),
        easing: 'easeOutExpo',
        duration: 1000
    }).finished;
}

/**
 * Animates the header elements on page load.
 * Creates a staggered appearance timeline for the logo, navigation links, and control icons.
 *
 * @returns {void} This function does not return a value.
 */
function animateHeader() {
    return anime({
        targets: 'header nav > *',
        opacity: [0, 1],
        translateY: [-30, 0],
        delay: anime.stagger(100),
        easing: 'easeOutExpo',
        duration: 800
    }).finished;
}

/**
 * Sets up an Intersection Observer to trigger animations when elements become visible.
 *
 * This function observes sections with the class `.animate-section`. When a
 * section enters the viewport, it checks for elements with the class
 * `.animate-card` within it. If cards are present, they are animated with a
 * staggered fade-in and slide-up effect. If no cards are found, the section
 * itself is animated. Once an element has been animated, it is unobserved to
 * prevent the animation from re-triggering.
 *
 * @returns {void} This function does not return a value.
 */
function setupIntersectionObserver() {
    const sections = document.querySelectorAll('.animate-section');
    if (sections.length === 0) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const cards = entry.target.querySelectorAll('.animate-card');
                const elements = cards.length > 0 ? Array.from(cards) : [entry.target];

                anime.timeline({
                    easing: 'easeOutExpo'
                })
                .add({
                    targets: elements,
                    opacity: [0, 1],
                    translateY: [100, 0],
                    duration: 1200,
                    delay: anime.stagger(150)
                });
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    sections.forEach(section => {
        observer.observe(section);
    });
}






/**
 * Sets up hover effects for the quick links in the footer.
 * On mouse-over, the link animates upwards. On mouse-out, it returns to its
 * original position and its color is restored based on the current theme
 * (light or dark mode).
 *
 * @returns {void} This function does not return a value.
 */
function setupQuickLinkHovers() {
    const quickLinks = document.querySelectorAll('.quick-link');
    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            anime({
                targets: link,
                translateY: -5,
                duration: 300,
                easing: 'easeOutExpo'
            });
        });

        link.addEventListener('mouseleave', () => {
            const isDarkMode = document.documentElement.classList.contains('dark');
            anime({
                targets: link,
                translateY: 0,
                color: isDarkMode ? 'rgba(255, 255, 255, 0.6)' : 'rgba(0, 0, 0, 0.6)',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
    });
}

/**
 * Sets up a hover animation for the site logo.
 * When the user hovers over the logo, it scales up slightly to provide
 * visual feedback. When the mouse leaves, it scales back to its original size.
 *
 * @returns {void} This function does not return a value.
 */
function setupLogoHoverAnimation() {
    const logos = document.querySelectorAll('.logo-container');
    logos.forEach(logo => {
        logo.addEventListener('mouseenter', () => {
            anime({
                targets: logo.querySelector('a'),
                scale: 1.05,
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
        logo.addEventListener('mouseleave', () => {
            anime({
                targets: logo.querySelector('a'),
                scale: 1,
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
    });
}

/**
 * Sets up the theme switcher functionality.
 * This function handles the theme toggle buttons, reads the user's preference
 * from localStorage, and applies the corresponding theme (light or dark). It
 * also adds event listeners to the buttons to allow theme switching.
 *
 * @returns {void} This function does not return a value.
 */
function setupThemeSwitcher() {
    const themeToggleButtons = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
    const htmlElement = document.documentElement;

    // Function to update the theme based on the isDarkMode flag
    const updateTheme = (isDarkMode) => {
        htmlElement.classList.toggle('dark', isDarkMode);
        themeToggleButtons.forEach(button => {
            if (button) {
                button.querySelector('span').textContent = isDarkMode ? 'dark_mode' : 'light_mode';
            }
        });
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    };

    // Initialize theme based on localStorage or default to light
    const storedTheme = localStorage.getItem('theme');
    const initialThemeIsDark = storedTheme === 'dark';
    updateTheme(initialThemeIsDark);

    // Add click listeners to the buttons
    themeToggleButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', () => {
                const isCurrentlyDark = htmlElement.classList.contains('dark');
                updateTheme(!isCurrentlyDark);
            });
        }
    });
}

// Initialize everything after the DOM is loaded.
document.addEventListener('DOMContentLoaded', () => {
    // Setup theme switcher first to ensure it runs even if animations fail
    setupThemeSwitcher();
    initializeWebsiteInteractivity();
});
