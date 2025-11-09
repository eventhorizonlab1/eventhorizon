/**
 * @file Central repository for all documented JavaScript functions,
 * including animations, theme switching, and other interactive features.
 * @author Jules
 */

// =================================================================================================
// Internationalization (i18n)
// =================================================================================================

/**
 * @property {object} translations - An object to store the loaded translation strings.
 */
let translations = {};

/**
 * Asynchronously loads a translation file for a given language.
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

    // --- Appel de la nouvelle fonction de particules ---
    setupParticleBackground();
}

/**
 * Animates the main title on page load.
 * The title fades in and slides down for a smooth entrance effect.
 *
 * @returns {Promise} A promise that resolves when the animation is finished.
 */
function animateMainTitle() {
    const mainTitle = document.querySelector('.main-title');
    if (!mainTitle) return Promise.resolve(); // Retourne une promesse résolue si l'élément n'existe pas

    const words = mainTitle.innerText.split(' ');
    mainTitle.innerHTML = words.map(word => `<span>${word}</span>`).join(' ');

    return anime({
        targets: '.main-title span',
        opacity: [0, 1],
        translateY: [50, 0],
        delay: anime.stagger(100),
        easing: 'easeOutExpo',
        duration: 1000
    }).finished; // --- Amélioration : retourne la promesse .finished ---
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
    }).finished; // --- Amélioration : retourne la promesse .finished ---
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

// ---
// --- NOUVELLE FONCTION AJOUTÉE ---
// ---
/**
 * Crée un fond de particules lent et discret pour la section principale.
 * @returns {void}
 */
function setupParticleBackground() {
    const container = document.getElementById('particle-container');
    if (!container) return; // Ne fait rien si le conteneur n'existe pas

    const numParticles = 50; // Ajustez ce nombre selon vos goûts (50 est un bon début)

    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        // Position initiale aléatoire
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;

        container.appendChild(particle);
    }

    // Animation avec anime.js
    anime({
        targets: '.particle',
        translateX: () => anime.random(-150, 150), // Dérive horizontale lente
        translateY: () => anime.random(-150, 150), // Dérive verticale lente
        opacity: [
            // Apparaît, reste visible, puis disparaît
            { value: 0, duration: 0 },
            { value: () => anime.random(0.1, 0.4), duration: () => anime.random(1000, 3000) }, // Fade in
            { value: 0, duration: () => anime.random(1000, 3000), delay: () => anime.random(15000, 25000) } // Fade out
        ],
        easing: 'linear',
        duration: () => anime.random(30000, 50000), // Durée très longue (30-50s)
        loop: true,
        delay: () => anime.random(0, 30000) // Départ décalé pour chaque particule
    });
}
// ---
// --- FIN DE LA NOUVELLE FONCTION ---
// ---


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
            anime({
                targets: link,
                translateY: 0,
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
    setupLanguageSwitcher();

    // Set default language to French
    setLanguage('fr');

    initializeWebsiteInteractivity();
});
