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
 * Links move up and change color on hover.
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

// Initialize everything after the DOM is loaded.
document.addEventListener('DOMContentLoaded', initializeWebsiteInteractivity);
