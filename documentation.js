/**
 * @file This script handles all the interactive elements of the Event Horizon website.
 * @description Enhanced version with advanced animations, accessibility, and performance.
 * @version 2.0.0
 */

/**
 * A global object to store the translations for the current language.
 * @type {Object<string, string>}
 */
let translations = {};

// ================================================================
// 🌍 Language Management
// ================================================================

/**
 * Asynchronously loads translations for a specified language from a JSON file.
 *
 * @description This function fetches a language file from the `locales/` directory and
 * populates the global `translations` object with the key-value pairs.
 * It includes error handling to catch network issues or problems parsing the JSON.
 *
 * @param {string} lang - The language code (e.g., 'en', 'fr') for the translations to load.
 * @returns {Promise<void>} A promise that resolves when the translations are loaded.
 */
async function loadTranslations(lang) {
  try {
    const response = await fetch(`locales/${lang}.json`);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    translations = await response.json();

    // Validation des données
    if (!translations || typeof translations !== 'object') {
      throw new Error('Invalid translation format');
    }

    announceToScreenReader(`Langue changée en ${lang === 'fr' ? 'français' : 'anglais'}`);

  } catch (error) {
    console.error(`Failed to load translations for ${lang}:`, error);

    // Fallback vers français si échec
    if (lang !== 'fr') {
      console.warn('Falling back to French...');
      await loadTranslations('fr');
    } else {
      // Afficher message utilisateur si échec critique
      const alertDiv = document.createElement('div');
      alertDiv.className = 'fixed top-4 right-4 bg-red-500 text-white p-4 rounded-lg z-50';
      alertDiv.textContent = 'Erreur de chargement des traductions';
      document.body.appendChild(alertDiv);
      setTimeout(() => alertDiv.remove(), 5000);
    }
  }
}

/**
 * Applies the currently loaded translations to all elements with `data-i18n-key`.
 *
 * @description This function iterates through all elements that have a `data-i18n-key`
 * attribute and sets their content or a specified attribute to the corresponding
 * value from the global `translations` object.
 *
 * @returns {void}
 */
function applyTranslations() {
  document.querySelectorAll("[data-i18n-key]").forEach((el) => {
    const key = el.getAttribute("data-i18n-key");
    const translation = translations[key];
    if (translation) {
      const attr = el.getAttribute("data-i18n-attr");
      if (attr) el.setAttribute(attr, translation);
      else el.textContent = translation;
    }
  });
}

/**
 * Sets the language of the website by loading and applying translations.
 *
 * @description This asynchronous function orchestrates the language change by first
 * loading the new translations, then applying them to the DOM, and finally
 * updating the UI of the language switcher to reflect the new active language.
 *
 * @param {string} lang - The language code (e.g., 'en', 'fr') to set as the active language.
 * @returns {Promise<void>} A promise that resolves when the language has been fully set.
 */
async function setLanguage(lang) {
  // Afficher loader
  const loader = document.createElement('div');
  loader.className = 'fixed inset-0 bg-black/20 flex items-center justify-center z-50';
  loader.innerHTML = '<div class="animate-spin rounded-full h-12 w-12 border-4 border-indigo-500 border-t-transparent"></div>';
  document.body.appendChild(loader);

  try {
    await loadTranslations(lang);
    applyTranslations();
    updateLanguageSwitcherUI(lang);
  } finally {
    loader.remove();
  }
}

/**
 * Updates the visual state of the language switcher UI.
 *
 * @description This function styles the language links to indicate which language is
 * currently active. It applies different classes based on whether a link's
 * language matches the `activeLang`.
 *
 * @param {string} activeLang - The language code of the currently active language.
 * @returns {void}
 */
function updateLanguageSwitcherUI(activeLang) {
  document.querySelectorAll("[data-lang]").forEach((link) => {
    const linkLang = link.getAttribute("data-lang");
    const isSelected = linkLang === activeLang;
    link.classList.toggle("text-light-text-primary", isSelected);
    link.classList.toggle("dark:text-dark-text-primary", isSelected);
    link.classList.toggle("text-light-text-secondary", !isSelected);
    link.classList.toggle("dark:text-dark-text-secondary", !isSelected);
    
    // Update ARIA attributes
    link.setAttribute('aria-pressed', isSelected ? 'true' : 'false');
    if (isSelected) {
      link.setAttribute('aria-current', 'true');
    } else {
      link.removeAttribute('aria-current');
    }
  });
}

/**
 * Sets up the event listener for the language switcher.
 *
 * @description This function finds the language switcher component in the DOM and attaches
 * a click event listener. When a language link is clicked, it calls
 * `setLanguage` to change the website's language.
 *
 * @returns {void}
 */
function setupLanguageSwitcher() {
  const switcher = document.querySelector(".language-switcher");
  if (!switcher) return;
  switcher.addEventListener("click", (e) => {
    if (e.target.matches("[data-lang]")) {
      e.preventDefault();
      const lang = e.target.getAttribute("data-lang");
      setLanguage(lang);
    }
  });
}

// ================================================================
// ♿ ACCESSIBILITY UTILITIES
// ================================================================

/**
 * Detects if the user prefers reduced motion.
 *
 * @returns {boolean} True if the user has requested reduced motion, false otherwise.
 */
function prefersReducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

/**
 * Returns an animation configuration adjusted for accessibility preferences.
 * If the user prefers reduced motion, the animation duration and delay are
 * set to minimal values.
 *
 * @param {object} config - The original anime.js configuration object.
 * @returns {object} The adjusted animation configuration.
 */
function getAccessibleAnimationConfig(config) {
  if (prefersReducedMotion()) {
    return {
      ...config,
      duration: 1,
      delay: 0,
    };
  }
  return config;
}

/**
 * Announces a message to screen readers using a visually hidden element.
 *
 * @param {string} message - The message to be announced.
 * @returns {void}
 */
function announceToScreenReader(message) {
  const announcement = document.createElement("div");
  announcement.setAttribute("role", "status");
  announcement.setAttribute("aria-live", "polite");
  announcement.classList.add("sr-only");
  announcement.textContent = message;

  document.body.appendChild(announcement);
  setTimeout(() => announcement.remove(), 1000);
}

/**
 * Sets up a listener to detect changes in the user's motion preference.
 * If the user enables "reduce motion", all running animations are stopped
 * and transformations are reset.
 *
 * @returns {void}
 */
function setupMotionPreferenceListener() {
  const motionMediaQuery = window.matchMedia("(prefers-reduced-motion: reduce)");

  motionMediaQuery.addEventListener("change", (e) => {
    if (e.matches) {
      // User just enabled "reduce motion"
      anime.remove("*");
      document.querySelectorAll("*").forEach((el) => {
        el.style.transform = "none";
        el.style.opacity = "1";
      });
    }
  });
}

/**
 * Traps focus within a given element for keyboard users.
 * This is useful for modals and mobile menus to prevent the focus from
 * escaping to the background content.
 *
 * @param {HTMLElement} element - The element to trap focus within.
 * @returns {void}
 */
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    "a[href], button:not([disabled]), textarea, input, select"
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  element.addEventListener("keydown", (e) => {
    if (e.key !== "Tab") return;

    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  });
}

/**
 * Sets up accessibility features for the mobile menu.
 * @description This function observes the mobile menu for visibility changes.
 * When the menu becomes visible, it applies the `trapFocus` function to keep
 * keyboard focus within the menu, improving accessibility.
 */
function setupMobileMenuAccessibility() {
  const mobileMenuToggle = document.querySelector('[x-on\\:click="menuOpen = !menuOpen"]');
  const mobileMenu = document.querySelector('.fixed.inset-y-0');

  if (!mobileMenuToggle || !mobileMenu) return;

  mobileMenuToggle.addEventListener('click', () => {
    setTimeout(() => {
      const isOpen = mobileMenu.offsetParent !== null;
      if (isOpen) {
        trapFocus(mobileMenu);
        mobileMenu.querySelector('a, button')?.focus();
      }
    }, 100);
  });

  // Fermer avec Escape
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && mobileMenu.offsetParent !== null) {
      mobileMenuToggle.click();
    }
  });
}

// ================================================================
// ✨ ENHANCED ANIMATIONS
// ================================================================

/**
 * Creates an enhanced page load animation sequence using spring physics and
 * advanced staggering. This provides a modern and engaging entry animation.
 *
 * @returns {anime.AnimeTimelineInstance} An anime.js timeline instance.
 */
function createEnhancedPageLoadAnimation() {
  const tl = anime.timeline({
    easing: "spring(1, 80, 10, 0)",
    duration: 1000,
  });

  // 1. Header fade in with drop effect
  tl.add(
    getAccessibleAnimationConfig({
      targets: "header",
      translateY: [-60, 0],
      opacity: [0, 1],
      duration: 1200,
      easing: "easeOutElastic(1, .8)",
    })
  );

  // 2. Main title with 3D effect
  tl.add(
    getAccessibleAnimationConfig({
      targets: ".main-title",
      opacity: [0, 1],
      scale: [0.8, 1],
      rotateX: [-20, 0],
      duration: 1500,
      easing: "easeOutExpo",
    }),
    "-=800"
  );

  // 3. Individual word animation with stagger
  tl.add(
    getAccessibleAnimationConfig({
      targets: ".main-title span",
      opacity: [0, 1],
      translateY: [30, 0],
      rotateZ: [-5, 0],
      delay: anime.stagger(80, {
        grid: [14, 1],
        from: "center",
      }),
      easing: "easeOutExpo",
    }),
    "-=1200"
  );

  return tl;
}

/**
 * Sets up enhanced scroll animations with a wave effect for elements with
 * the 'animate-section' class. Animations are triggered on intersection.
 *
 * @returns {void}
 */
function setupEnhancedScrollAnimations() {
  const sections = document.querySelectorAll(".animate-section");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const cards = entry.target.querySelectorAll(".animate-card");

          anime(
            getAccessibleAnimationConfig({
              targets: cards,
              opacity: [0, 1],
              translateY: [60, 0],
              rotateX: [-15, 0],
              scale: [0.9, 1],
              duration: 1200,
              delay: anime.stagger(120, {
                start: 200,
                easing: "easeOutQuad",
              }),
              easing: "spring(1, 80, 10, 0)",
            })
          );

          observer.unobserve(entry.target);
        }
      });
    },
    {
      threshold: 0.15,
      rootMargin: "0px 0px -80px 0px",
    }
  );

  sections.forEach((s) => observer.observe(s));
}

/**
 * Adds a subtle, continuous "breathing" animation to the site logo.
 * This animation is disabled if the user prefers reduced motion.
 *
 * @returns {void}
 */
function addLogoBreathingAnimation() {
  if (prefersReducedMotion()) return;

  const logos = document.querySelectorAll(".logo-container a");

  logos.forEach((logo) => {
    anime({
      targets: logo,
      scale: [1, 1.02, 1],
      duration: 3000,
      easing: "easeInOutSine",
      loop: true,
    });
  });
}

/**
 * Animates the main title of the page with a staggered word effect.
 *
 * @returns {anime.AnimeInstance | undefined} An anime.js animation instance, or undefined if the main title is not found.
 */
function animateMainTitle() {
  const mainTitle = document.querySelector(".main-title");
  if (!mainTitle) return;

  const words = mainTitle.innerText.split(" ");
  mainTitle.innerHTML = words.map((w) => `<span>${w}</span>`).join(" ");

  return anime(getAccessibleAnimationConfig({
    targets: ".main-title span",
    opacity: [0, 1],
    translateY: [50, 0],
    delay: anime.stagger(100),
    easing: "easeOutExpo",
    duration: 1000,
  }));
}

/**
 * Animates the navigation elements in the header.
 *
 * @returns {anime.AnimeInstance} An anime.js animation instance.
 */
function animateHeader() {
  return anime(getAccessibleAnimationConfig({
    targets: "header nav > *",
    opacity: [0, 1],
    translateY: [-30, 0],
    delay: anime.stagger(100),
    easing: "easeOutExpo",
    duration: 800,
  }));
}

/**
 * Animates all section titles with a fade-in and slide-up effect.
 *
 * @returns {void}
 */
function animateSectionTitles() {
  const titles = document.querySelectorAll("section h2");
  if (titles.length === 0) return;
  anime(getAccessibleAnimationConfig({
    targets: titles,
    opacity: [0, 1],
    translateY: [30, 0],
    delay: anime.stagger(200),
    duration: 1000,
    easing: "easeOutExpo",
  }));
}

// ================================================================
// 🎨 ADVANCED MICRO-INTERACTIONS
// ================================================================

/**
 * Sets up advanced hover effects for cards with a parallax effect.
 * The card and its image tilt based on the mouse position, creating a 3D
 * effect. This is disabled if the user prefers reduced motion.
 *
 * @returns {void}
 */
function setupAdvancedCardHovers() {
  if (prefersReducedMotion()) return;

  const cards = document.querySelectorAll(".animate-card a, .article-card");

  cards.forEach((card) => {
    const image = card.querySelector("img");
    const title = card.querySelector("h3");

    // Parallax on mouse move
    card.addEventListener("mousemove", (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = (y - centerY) / 20;
      const rotateY = (centerX - x) / 20;

      anime({
        targets: card,
        rotateX: rotateX,
        rotateY: rotateY,
        duration: 300,
        easing: "easeOutQuad",
      });

      if (image) {
        anime({
          targets: image,
          translateX: (x - centerX) / 30,
          translateY: (y - centerY) / 30,
          scale: 1.1,
          duration: 300,
          easing: "easeOutQuad",
        });
      }

      if (title) {
        anime({
          targets: title,
          translateY: -5,
          duration: 300,
          easing: "easeOutQuad",
        });
      }
    });

    card.addEventListener("mouseleave", () => {
      anime({
        targets: card,
        rotateX: 0,
        rotateY: 0,
        duration: 600,
        easing: "spring(1, 80, 10, 0)",
      });

      if (image) {
        anime({
          targets: image,
          translateX: 0,
          translateY: 0,
          scale: 1,
          duration: 600,
          easing: "spring(1, 80, 10, 0)",
        });
      }

      if (title) {
        anime({
          targets: title,
          translateY: 0,
          duration: 600,
          easing: "spring(1, 80, 10, 0)",
        });
      }
    });

    card.style.transformStyle = "preserve-3d";
    card.style.perspective = "1000px";
  });
}

/**
 * Sets up a magnetic effect for buttons. The button moves towards the mouse
 * pointer, creating a "magnetic" feel. This is disabled if the user prefers
 * reduced motion.
 *
 * @returns {void}
 */
function setupMagneticButtons() {
  if (prefersReducedMotion()) return;

  const buttons = document.querySelectorAll("button:not([disabled]), a.border");

  buttons.forEach((button) => {
    button.addEventListener("mousemove", (e) => {
      const rect = button.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;

      anime({
        targets: button,
        translateX: x * 0.3,
        translateY: y * 0.3,
        duration: 300,
        easing: "easeOutQuad",
      });
    });

    button.addEventListener("mouseleave", () => {
      anime({
        targets: button,
        translateX: 0,
        translateY: 0,
        duration: 600,
        easing: "spring(1, 80, 10, 0)",
      });
    });
  });
}

/**
 * Sets up hover animations for the quick links in the footer.
 *
 * @returns {void}
 */
function setupQuickLinkHovers() {
  const links = document.querySelectorAll(".quick-link");
  links.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      anime(getAccessibleAnimationConfig({ 
        targets: link, 
        translateY: -5, 
        duration: 300, 
        easing: "easeOutExpo" 
      }));
    });
    link.addEventListener("mouseleave", () => {
      const isDark = document.documentElement.classList.contains("dark");
      anime(getAccessibleAnimationConfig({
        targets: link,
        translateY: 0,
        color: isDark ? "rgba(255,255,255,0.6)" : "rgba(0,0,0,0.6)",
        duration: 300,
        easing: "easeOutExpo",
      }));
    });
  });
}

/**
 * Sets up generic hover animations for various interactive elements.
 *
 * @returns {void}
 */
function setupHoverAnimations() {
  const hoverables = document.querySelectorAll(".btn, .group.block");
  hoverables.forEach((el) => {
    el.addEventListener("mouseenter", () => {
      anime(getAccessibleAnimationConfig({ 
        targets: el, 
        scale: 1.05, 
        duration: 300, 
        easing: "easeOutQuad" 
      }));
    });
    el.addEventListener("mouseleave", () => {
      anime(getAccessibleAnimationConfig({ 
        targets: el, 
        scale: 1, 
        duration: 300, 
        easing: "easeOutQuad" 
      }));
    });
  });
}

/**
 * Sets up a hover animation for the site logo.
 *
 * @returns {void}
 */
function setupLogoHoverAnimation() {
  const logos = document.querySelectorAll(".logo-container");
  logos.forEach((logo) => {
    const link = logo.querySelector("a");
    if (!link) return;
    logo.addEventListener("mouseenter", () =>
      anime(getAccessibleAnimationConfig({ 
        targets: link, 
        scale: 1.05, 
        duration: 300, 
        easing: "easeOutExpo" 
      }))
    );
    logo.addEventListener("mouseleave", () =>
      anime(getAccessibleAnimationConfig({ 
        targets: link, 
        scale: 1, 
        duration: 300, 
        easing: "easeOutExpo" 
      }))
    );
  });
}

// ================================================================
// 🎯 ACCESSIBLE CAROUSEL
// ================================================================

/**
 * Sets up an accessible carousel with keyboard and button navigation.
 * This function is designed to be reusable for any carousel in the DOM.
 *
 * @param {string} selector - The CSS selector for the section containing the carousel.
 * @returns {void}
 */
function setupAccessibleCarousel(selector) {
  const section = document.querySelector(selector);
  if (!section) return;

  const container = section.querySelector(".flex.snap-x");
  const prevBtn = section.querySelector(
    "button .material-symbols-outlined"
  )?.parentElement;
  const nextBtn = section.querySelectorAll(
    "button .material-symbols-outlined"
  )[1]?.parentElement;
  const indicators = section.querySelectorAll(".mt-8 button");
  const cards = container.querySelectorAll(".animate-card, .flex-shrink-0");

  let currentIndex = 0;

  function scrollToCard(index) {
    if (index < 0 || index >= cards.length) return;

    currentIndex = index;
    const card = cards[index];

    card.scrollIntoView({
      behavior: prefersReducedMotion() ? "auto" : "smooth",
      block: "nearest",
      inline: "start",
    });

    updateIndicators();
    updateNavigationButtons();
    announceToScreenReader(
      `Affichage de l'élément ${index + 1} sur ${cards.length}`
    );
  }

  function updateIndicators() {
    const cardsPerView = Math.floor(container.offsetWidth / cards[0].offsetWidth);
    indicators.forEach((indicator, i) => {
      const isActive = i === Math.floor(currentIndex / cardsPerView);
      indicator.classList.toggle("bg-black", isActive);
      indicator.classList.toggle("dark:bg-white", isActive);
      indicator.classList.toggle("bg-gray-300", !isActive);
      indicator.setAttribute("aria-pressed", isActive ? "true" : "false");
    });
  }

  function updateNavigationButtons() {
    if (prevBtn) {
      prevBtn.disabled = currentIndex === 0;
      prevBtn.setAttribute(
        "aria-label",
        currentIndex === 0 ? "Début du carrousel" : "Élément précédent"
      );
    }

    if (nextBtn) {
      nextBtn.disabled = currentIndex >= cards.length - 1;
      nextBtn.setAttribute(
        "aria-label",
        currentIndex >= cards.length - 1 ? "Fin du carrousel" : "Élément suivant"
      );
    }
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", () => {
      scrollToCard(Math.max(0, currentIndex - 1));
    });
  }

  if (nextBtn) {
    nextBtn.addEventListener("click", () => {
      scrollToCard(Math.min(cards.length - 1, currentIndex + 1));
    });
  }

  indicators.forEach((indicator, i) => {
    indicator.addEventListener("click", () => {
      const cardsPerView = Math.floor(
        container.offsetWidth / cards[0].offsetWidth
      );
      scrollToCard(i * cardsPerView);
    });
    indicator.setAttribute("aria-label", `Aller au groupe ${i + 1}`);
  });

  container.addEventListener("keydown", (e) => {
    switch (e.key) {
      case "ArrowLeft":
        e.preventDefault();
        scrollToCard(currentIndex - 1);
        break;
      case "ArrowRight":
        e.preventDefault();
        scrollToCard(currentIndex + 1);
        break;
      case "Home":
        e.preventDefault();
        scrollToCard(0);
        break;
      case "End":
        e.preventDefault();
        scrollToCard(cards.length - 1);
        break;
    }
  });

  let scrollTimeout;
  container.addEventListener("scroll", () => {
    clearTimeout(scrollTimeout);
    scrollTimeout = setTimeout(() => {
      const scrollLeft = container.scrollLeft;
      const cardWidth = cards[0].offsetWidth;
      currentIndex = Math.round(scrollLeft / cardWidth);
      updateIndicators();
      updateNavigationButtons();
    }, 100);
  });

  container.setAttribute("tabindex", "0");
  container.setAttribute("role", "region");
  container.setAttribute("aria-label", "Carrousel d'articles");

  updateIndicators();
  updateNavigationButtons();
}

// ================================================================
// 📊 READING PROGRESS BAR
// ================================================================

/**
 * Sets up a reading progress bar at the top of the page.
 * The bar's width and color change as the user scrolls.
 *
 * @returns {void}
 */
function setupReadingProgress() {
  const progressBar = document.getElementById("reading-progress");
  if (!progressBar) return;

  let ticking = false;

  function updateProgress() {
    const windowHeight = window.innerHeight;
    const documentHeight =
      document.documentElement.scrollHeight - windowHeight;
    const scrolled = window.scrollY;
    const progress = (scrolled / documentHeight) * 100;

    progressBar.style.width = `${Math.min(progress, 100)}%`;
    progressBar.setAttribute("aria-valuenow", Math.round(progress));

    if (progress < 33) {
      progressBar.style.background =
        "linear-gradient(to right, #6366F1, #8B5CF6)";
    } else if (progress < 66) {
      progressBar.style.background =
        "linear-gradient(to right, #8B5CF6, #EC4899)";
    } else {
      progressBar.style.background =
        "linear-gradient(to right, #EC4899, #F59E0B)";
    }

    ticking = false;
  }

  window.addEventListener("scroll", () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        updateProgress();
      });
      ticking = true;
    }
  });

  updateProgress();
}

// ================================================================
// 🎨 THEME MANAGEMENT
// ================================================================

/**
 * Updates ARIA attributes for theme toggle buttons.
 * @param {boolean} isDark - Whether dark mode is active
 */
function updateThemeToggleAria(isDark) {
  const buttons = document.querySelectorAll('#theme-toggle, #theme-toggle-mobile');
  buttons.forEach(btn => {
    btn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    btn.setAttribute('aria-label', 
      isDark ? 'Activer le mode clair' : 'Activer le mode sombre'
    );
  });
}

/**
 * Sets up the theme switcher functionality.
 *
 * @returns {void}
 */
function setupThemeSwitcher() {
  const buttons = document.querySelectorAll("#theme-toggle, #theme-toggle-mobile");
  const html = document.documentElement;

  const updateTheme = (isDark, explicit = true) => {
    html.classList.toggle("dark", isDark);
    
    buttons.forEach((btn) => {
      const icon = btn.querySelector("span");
      if (icon) {
        icon.textContent = isDark ? "dark_mode" : "light_mode";
      }
    });
    
    updateThemeToggleAria(isDark);
    
    if (explicit) {
      localStorage.setItem("theme", isDark ? "dark" : "light");
    }
  };

  const isDark = html.classList.contains("dark");
  buttons.forEach((btn) => {
    const icon = btn.querySelector("span");
    if (icon) {
      icon.textContent = isDark ? "dark_mode" : "light_mode";
    }
  });
  updateThemeToggleAria(isDark);

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const currentlyDark = html.classList.contains("dark");
      updateTheme(!currentlyDark, true);
    });
  });
}

// ================================================================
// ✨ NEW FEATURES
// ================================================================

/**
 * Animates numbers for statistics, counting up from zero to the target value.
 * This is triggered for elements with the 'data-stat-value' attribute.
 *
 * @returns {void}
 */
function animateNumbers() {
  const statElements = document.querySelectorAll("[data-stat-value]");

  statElements.forEach((el) => {
    const targetValue = parseInt(el.getAttribute("data-stat-value"));
    const obj = { value: 0 };

    anime({
      targets: obj,
      value: targetValue,
      duration: 2000,
      easing: "easeOutExpo",
      round: 1,
      update: () => {
        el.textContent = obj.value.toLocaleString();
      },
    });
  });
}

/**
 * Sets up a morphing SVG logo animation on hover.
 * The SVG path morphs to a different shape, creating a playful effect.
 *
 * @returns {void}
 */
function setupLogoMorph() {
  const logo = document.querySelector(".logo-container svg");
  if (!logo) return;

  logo.addEventListener("mouseenter", () => {
    anime({
      targets: ".logo-container svg path",
      d: [
        { value: logo.querySelector("path").getAttribute("d") },
        { value: "M10,10 L90,10 L90,90 L10,90 Z" }, // Forme cible
      ],
      duration: 800,
      easing: "easeInOutQuad",
      direction: "alternate",
    });
  });
}

/**
 * Sets up social sharing functionality for buttons with the 'data-share' attribute.
 * Uses the Web Share API if available, otherwise falls back to copying the URL
 * to the clipboard.
 *
 * @returns {void}
 */
function setupSocialShare() {
  const shareButtons = document.querySelectorAll("[data-share]");

  shareButtons.forEach((btn) => {
    btn.addEventListener("click", async () => {
      const url = window.location.href;
      const title = document.title;

      if (navigator.share) {
        await navigator.share({ title, url });
      } else {
        // Fallback : copier le lien
        await navigator.clipboard.writeText(url);
        announceToScreenReader("Lien copié dans le presse-papier");
      }
    });
  });
}

/**
 * Sets up the search modal functionality, including opening and closing the modal.
 * The search logic itself is a placeholder (TODO).
 *
 * @returns {void}
 */
function setupSearchModal() {
  // TODO: Implement search logic (e.g., fetching from an API).
  // This is a placeholder for demonstration purposes. The UI is in place,
  // but the search functionality is not yet implemented.
  const searchToggle = document.getElementById("search-toggle");
  const searchModal = document.getElementById("search-modal");
  const searchInput = searchModal.querySelector("input");

  if (!searchToggle || !searchModal) return;

  searchToggle.addEventListener("click", () => {
    searchModal.classList.remove("hidden");
    searchInput.focus();
  });

  searchModal.addEventListener("click", (e) => {
    if (e.target === searchModal) {
      searchModal.classList.add("hidden");
    }
  });
}

// ================================================================
// 🚀 INITIALIZATION
// ================================================================

/**
 * Initializes all website interactivity.
 */
function initializeWebsiteInteractivity() {
  if (prefersReducedMotion()) {
    document.querySelectorAll('[style*="opacity"]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }
  
  createEnhancedPageLoadAnimation();
  setupEnhancedScrollAnimations();
  addLogoBreathingAnimation();
  setupQuickLinkHovers();
  setupLogoHoverAnimation();
  setupHoverAnimations();
  setupAdvancedCardHovers();
  setupMagneticButtons();
  animateSectionTitles();
}

document.addEventListener("DOMContentLoaded", () => {
  setupMobileMenuAccessibility();
  setupMotionPreferenceListener();
  setupThemeSwitcher();
  setupLanguageSwitcher();
  setupReadingProgress();
  setLanguage("fr");
  setupSearchModal();
  setupSocialShare();
  setupLogoMorph();
  animateNumbers();

  if (document.getElementById("particle-container")) {
    initializeWebsiteInteractivity();
  }
  
  setupAccessibleCarousel('#articles');
  setupAccessibleCarousel('#ecosysteme');
});
