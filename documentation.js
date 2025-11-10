/**
 * @file This file is the central repository for all JavaScript functions
 * responsible for the interactivity and animations of the Event Horizon website.
 * It handles internationalization (i18n), animations, theme switching,
 * and other dynamic features.
 *
 * @author Jules
 * @see <a href="https://animejs.com/">anime.js</a> for the animation library used.
 * @see <a href="https://alpinejs.dev/">Alpine.js</a> for the framework used for interactivity.
 */

// =================================================================================================
// Internationalization (i18n)
// =================================================================================================

/**
 * An object to store the loaded translation strings.
 * @property {object} translations
 */
let translations = {};

/**
 * Asynchronously loads a translation file for a given language.
 *
 * @param {string} lang - The language code (e.g., 'fr', 'en').
 * @returns {Promise<void>} A promise that resolves when translations are loaded.
 */
async function loadTranslations(lang) {
    try {
        const response = await fetch(`locales/${lang}.json`);
        if (!response.ok) {
            throw new Error(`Network response was not ok for ${lang}.json`);
        }
        translations = await response.json();
    } catch (error) {
        console.error('Failed to load translations:', error);
    }
}

/**
 * Applies the currently loaded translations to all elements with `data-i18n-key`.
 *
 * @returns {void}
 */
function applyTranslations() {
    document.querySelectorAll('[data-i18n-key]').forEach(element => {
        const key = element.getAttribute('data-i18n-key');
        const translation = translations[key];

        if (translation) {
            const attr = element.getAttribute('data-i18n-attr');
            if (attr) {
                element.setAttribute(attr, translation);
            } else {
                element.textContent = translation;
            }
        }
    });
}

/**
 * Sets the application language, loads and applies translations.
 *
 * @param {string} lang - The language to switch to ('fr' or 'en').
 * @returns {Promise<void>}
 */
async function setLanguage(lang) {
    await loadTranslations(lang);
    applyTranslations();
    updateLanguageSwitcherUI(lang);
}

/**
 * Updates the UI of the language switcher to highlight the active language.
 *
 * @param {string} activeLang - The currently active language code.
 * @returns {void}
 */
function updateLanguageSwitcherUI(activeLang) {
    document.querySelectorAll('[data-lang]').forEach(link => {
        const linkLang = link.getAttribute('data-lang');
        const isSelected = linkLang === activeLang;

        link.classList.toggle('text-light-text-primary', isSelected);
        link.classList.toggle('dark:text-dark-text-primary', isSelected);
        link.classList.toggle('text-light-text-secondary', !isSelected);
        link.classList.toggle('dark:text-dark-text-secondary', !isSelected);
    });
}

/**
 * Initializes the language switcher event listeners.
 *
 * @returns {void}
 */
function setupLanguageSwitcher() {
    document.querySelector('.language-switcher').addEventListener('click', (event) => {
        if (event.target.matches('[data-lang]')) {
            event.preventDefault();
            const lang = event.target.getAttribute('data-lang');
            setLanguage(lang);
        }
    });
}


// =================================================================================================
// Animations & Interactivity
// =================================================================================================

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
 * @returns {Promise} A promise that resolves when the animation is finished.
 */
function animateMainTitle() {
    const mainTitle = document.querySelector('.main-title');
    if (!mainTitle) return Promise.resolve();

    const words = mainTitle.innerText.split(' ');
    mainTitle.innerHTML = words.map(word => `<span>${word}</span>`).join(' ');

    return anime({
        targets: '.main-title span',
        opacity: [0, 1],
        translateY: [50, 0],
        delay: anime.stagger(100),
        easing: 'easeOutExpo',
        duration: 1000
    });
}

/**
 * Animates the header elements on page load.
 * Creates a staggered appearance timeline for the logo, navigation links, and control icons.
 *
 * @returns {Promise} A promise that resolves when the animation is finished.
 */
function animateHeader() {
    return anime({
        targets: 'header nav > *',
        opacity: [0, 1],
        translateY: [-30, 0],
        delay: anime.stagger(100),
        easing: 'easeOutExpo',
        duration: 800
    });
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
 * Creates a slow and subtle particle background for the main section.
 * This function generates a specified number of particle elements and animates
 * them to create a drifting effect. The particles fade in and out over a long
 * duration, creating a gentle and unobtrusive background animation.
 *
 * @returns {void} This function does not return a value.
 */

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

    /**
     * Updates the theme based on the provided isDarkMode flag.
     * @param {boolean} isDarkMode - A boolean indicating whether to apply the dark mode.
     * @returns {void}
     */
    const updateTheme = (isDarkMode) => {
        htmlElement.classList.toggle('dark', isDarkMode);
        themeToggleButtons.forEach(button => {
            if (button) {
                button.querySelector('span').textContent = isDarkMode ? 'dark_mode' : 'light_mode';
            }
        });
        localStorage.setItem('theme', isDarkMode ? 'dark' : 'light');
    };

    const storedTheme = localStorage.getItem('theme');
    const initialThemeIsDark = storedTheme === 'dark';
    updateTheme(initialThemeIsDark);

    themeToggleButtons.forEach(button => {
        if (button) {
            button.addEventListener('click', () => {
                const isCurrentlyDark = htmlElement.classList.contains('dark');
                updateTheme(!isCurrentlyDark);
            });
        }
    });
}

/**
 * Initializes the website's interactivity.
 * This function is the entry point for all client-side JavaScript.
 * It sets up the theme switcher, language switcher, and all animations.
 */
document.addEventListener('DOMContentLoaded', () => {
    setupThemeSwitcher();
    setupLanguageSwitcher();
    setLanguage('fr');
    initializeWebsiteInteractivity();
});
