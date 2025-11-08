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
    setupMenuItemHovers();
    setupLogoHoverAnimation();
    setupBackToTopButton();
    setupHeaderScrollAnimation();
    setupLazyLoading();
    setupThemeSwitcher();
}

/**
 * Sets up the theme switcher functionality.
 * The theme switcher allows the user to toggle between light and dark modes.
 * The selected theme is saved to localStorage to persist across sessions.
 * @returns {void} This function does not return a value.
 */
function setupThemeSwitcher() {
    const themeSwitcher = document.getElementById('theme-switcher');
    if (!themeSwitcher) return;

    const sunIcon = themeSwitcher.querySelector('.sun-icon');
    const moonIcon = themeSwitcher.querySelector('.moon-icon');

    const savedTheme = localStorage.getItem('theme');

    // Default to light theme if no theme is saved
    let isDark = savedTheme === 'dark';

    function updateTheme(isDark) {
        if (isDark) {
            document.documentElement.classList.add('dark');
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.classList.remove('dark');
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
            localStorage.setItem('theme', 'light');
        }
    }

    // Set initial theme
    updateTheme(isDark);

    themeSwitcher.addEventListener('click', () => {
        isDark = !isDark;
        updateTheme(isDark);
    });
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
 * Sets up a hover animation for the logo.
 * Creates a subtle distortion effect on hover to add a modern touch.
 *
 * @returns {void} This function does not return a value.
 */
function setupLogoHoverAnimation() {
    const logos = document.querySelectorAll('.logo-container');
    logos.forEach(logo => {
        logo.addEventListener('mouseenter', () => {
            anime({
                targets: logo.querySelector('a'),
                color: '#FFFFFF',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
        logo.addEventListener('mouseleave', () => {
            anime({
                targets: logo.querySelector('a'),
                color: '#B0B0B0',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
    });
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
 * Sets up an Intersection Observer to animate elements as they enter the viewport.
 * Sections without cards fade in and slide up.
 * Cards within sections fade in and slide up with a staggered delay for a dynamic effect.
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
 * Links move up and change color on hover for a clear visual cue.
 *
 * @returns {void} This function does not return a value.
 */
function setupQuickLinkHovers() {
    const quickLinks = document.querySelectorAll('.quick-link');

    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            link.classList.add('text-primary');
            anime({
                targets: link,
                translateY: -5,
                duration: 300,
                ease: 'easeOutExpo'
            });
        });

        link.addEventListener('mouseleave', () => {
            link.classList.remove('text-primary');
            anime({
                targets: link,
                translateY: 0,
                duration: 300,
                ease: 'easeOutExpo'
            });
        });
    });
}

/**
 * Sets up hover effects for the menu items in the header.
 * Links move up and change color on hover for a clear visual cue.
 *
 * @returns {void} This function does not return a value.
 */
function setupMenuItemHovers() {
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(link => {
        link.addEventListener('mouseenter', () => {
            link.classList.remove('text-white');
            link.classList.add('text-primary');
            anime({
                targets: link,
                translateY: -5,
                duration: 300,
                ease: 'easeOutExpo'
            });
        });

        link.addEventListener('mouseleave', () => {
            link.classList.remove('text-primary');
            link.classList.add('text-white');
            anime({
                targets: link,
                translateY: 0,
                duration: 300,
                ease: 'easeOutExpo'
            });
        });
    });
}

/**
 * Sets up the "Back to Top" button functionality.
 * The button appears on scroll and smoothly scrolls to the top when clicked,
 * improving navigation on long pages.
 *
 * @returns {void} This function does not return a value.
 */
function setupBackToTopButton() {
    const backToTopButton = document.getElementById('back-to-top');
    if (!backToTopButton) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopButton.classList.add('show');
        } else {
            backToTopButton.classList.remove('show');
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Sets up a scroll animation for the header.
 * Adds a 'scrolled' class to the header when the user scrolls down,
 * providing a visual cue that the header is in a fixed state.
 *
 * @returns {void} This function does not return a value.
 */
function setupHeaderScrollAnimation() {
    const header = document.querySelector('header');
    if (!header) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
}

/**
 * Sets up lazy loading for images and divs with background images.
 * Elements with the 'lazy' class will be loaded only when they enter the viewport,
 * improving page load performance.
 *
 * @returns {void} This function does not return a value.
 */
function setupLazyLoading() {
    const lazyElements = document.querySelectorAll('.lazy');

    if ('IntersectionObserver' in window) {
        let lazyElementObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    let lazyElement = entry.target;
                    if (lazyElement.tagName === 'IMG') {
                        lazyElement.src = lazyElement.dataset.src;
                    } else {
                        lazyElement.style.backgroundImage = lazyElement.dataset.src;
                    }
                    lazyElement.classList.remove('lazy');
                    lazyElementObserver.unobserve(lazyElement);
                }
            });
        });

        lazyElements.forEach((lazyElement) => {
            lazyElementObserver.observe(lazyElement);
        });
    } else {
        // Fallback for browsers that don't support IntersectionObserver
        lazyElements.forEach((lazyElement) => {
            if (lazyElement.tagName === 'IMG') {
                lazyElement.src = lazyElement.dataset.src;
            } else {
                lazyElement.style.backgroundImage = lazyElement.dataset.src;
            }
            lazyElement.classList.remove('lazy');
        });
    }
}

// Initialize everything after the DOM is loaded.
document.addEventListener('DOMContentLoaded', initializeWebsiteInteractivity);
