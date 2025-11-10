/**
 * @file Centralise toutes les fonctions d'interactivité et d'animation
 * du site Event Horizon. Inclut la gestion du thème, des langues, et des
 * effets visuels propulsés par Anime.js.
 *
 * @author Jules
 * @see https://animejs.com/
 */

// =================================================================================================
// 🌍 Internationalisation (i18n)
// =================================================================================================

/**
 * An object to store the translations.
 * @type {Object}
 */
let translations = {};

/**
 * Loads the translation file for the specified language.
 *
 * @param {string} lang - The language to load (e.g., 'en', 'fr').
 * @returns {Promise<void>} A promise that resolves when the translations are loaded.
 */
async function loadTranslations(lang) {
  try {
    const response = await fetch(`locales/${lang}.json`);
    if (!response.ok) throw new Error(`Network response was not ok for ${lang}.json`);
    translations = await response.json();
  } catch (error) {
    console.error("Failed to load translations:", error);
  }
}

/**
 * Applies the loaded translations to all elements with the 'data-i18n-key' attribute.
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
 * Sets the language of the website.
 *
 * @param {string} lang - The language to set (e.g., 'en', 'fr').
 * @returns {Promise<void>} A promise that resolves when the language is set.
 */
async function setLanguage(lang) {
  await loadTranslations(lang);
  applyTranslations();
  updateLanguageSwitcherUI(lang);
}

/**
 * Updates the UI of the language switcher to reflect the active language.
 *
 * @param {string} activeLang - The currently active language.
 */
function updateLanguageSwitcherUI(activeLang) {
  document.querySelectorAll("[data-lang]").forEach((link) => {
    const linkLang = link.getAttribute("data-lang");
    const isSelected = linkLang === activeLang;
    link.classList.toggle("text-light-text-primary", isSelected);
    link.classList.toggle("dark:text-dark-text-primary", isSelected);
    link.classList.toggle("text-light-text-secondary", !isSelected);
    link.classList.toggle("dark:text-dark-text-secondary", !isSelected);
  });
}

/**
 * Sets up the language switcher to handle clicks on the language links.
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

// =================================================================================================
// ✨ Animations & Interactivité
// =================================================================================================

/**
 * Initializes all website interactivity, including animations and event listeners.
 */
function initializeWebsiteInteractivity() {
  const timeline = anime.timeline({
    easing: "easeOutExpo",
    duration: 1000,
  });

  timeline.add(animateHeader()).add(animateMainTitle(), "-=500");

  setupIntersectionObserver();
  setupQuickLinkHovers();
  setupLogoHoverAnimation();
  initializeDotsGrid();
  setupHoverAnimations(); // 🔹 nouveau
  animateSectionTitles(); // 🔹 nouveau
}

/**
 * Initializes the animated dots grid in the background.
 */
function initializeDotsGrid() {
  const container = document.querySelector(".dots-grid");
  if (!container) return;

  const gridSize = 20;
  for (let i = 0; i < gridSize * gridSize; i++) {
    const dot = document.createElement("div");
    dot.className = "dot";
    container.appendChild(dot);
  }

  anime.timeline({ easing: "easeInOutQuad", loop: true }).add({
    targets: ".dot",
    scale: [{ value: 0.5, duration: 0 }, { value: [0.5, 1.5, 0.5], duration: 2000 }],
    opacity: [{ value: 0.3, duration: 0 }, { value: [0.3, 1, 0.3], duration: 2000 }],
    delay: anime.stagger(30, { grid: [gridSize, gridSize], from: "center" }),
  });
}

/**
 * Animates the main title of the page.
 * @returns {anime.AnimeInstance} The anime.js animation instance.
 */
function animateMainTitle() {
  const mainTitle = document.querySelector(".main-title");
  if (!mainTitle) return;

  const words = mainTitle.innerText.split(" ");
  mainTitle.innerHTML = words.map((w) => `<span>${w}</span>`).join(" ");

  return anime({
    targets: ".main-title span",
    opacity: [0, 1],
    translateY: [50, 0],
    delay: anime.stagger(100),
    easing: "easeOutExpo",
    duration: 1000,
  });
}

/**
 * Animates the header of the page.
 * @returns {anime.AnimeInstance} The anime.js animation instance.
 */
function animateHeader() {
  return anime({
    targets: "header nav > *",
    opacity: [0, 1],
    translateY: [-30, 0],
    delay: anime.stagger(100),
    easing: "easeOutExpo",
    duration: 800,
  });
}

/**
 * Sets up an intersection observer to animate sections as they scroll into view.
 */
function setupIntersectionObserver() {
  const sections = document.querySelectorAll(".animate-section");
  if (sections.length === 0) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const cards = entry.target.querySelectorAll(".animate-card");
          const targets = cards.length ? cards : [entry.target];

          anime({
            targets,
            opacity: [0, 1],
            translateY: [80, 0],
            duration: 1200,
            delay: anime.stagger(150),
            easing: "easeOutExpo",
          });

          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.1, rootMargin: "0px 0px -50px 0px" }
  );

  sections.forEach((section) => observer.observe(section));
}

/**
 * Animates the titles of the sections.
 */
function animateSectionTitles() {
  const titles = document.querySelectorAll("section h2");
  if (titles.length === 0) return;

  anime({
    targets: titles,
    opacity: [0, 1],
    translateY: [30, 0],
    delay: anime.stagger(200),
    duration: 1000,
    easing: "easeOutExpo",
  });
}

/**
 * Sets up the hover animation for the quick links in the footer.
 */
function setupQuickLinkHovers() {
  const links = document.querySelectorAll(".quick-link");
  links.forEach((link) => {
    link.addEventListener("mouseenter", () => {
      anime({ targets: link, translateY: -5, duration: 300, easing: "easeOutExpo" });
    });
    link.addEventListener("mouseleave", () => {
      const isDark = document.documentElement.classList.contains("dark");
      anime({
        targets: link,
        translateY: 0,
        color: isDark ? "rgba(255,255,255,0.6)" : "rgba(0,0,0,0.6)",
        duration: 300,
        easing: "easeOutExpo",
      });
    });
  });
}

/**
 * Sets up the hover animation for cards and buttons.
 */
function setupHoverAnimations() {
  const hoverables = document.querySelectorAll(".btn, .article-card, .group.block");
  hoverables.forEach((el) => {
    el.addEventListener("mouseenter", () => {
      anime({ targets: el, scale: 1.05, duration: 300, easing: "easeOutQuad" });
    });
    el.addEventListener("mouseleave", () => {
      anime({ targets: el, scale: 1, duration: 300, easing: "easeOutQuad" });
    });
  });
}

/**
 * Sets up the hover animation for the logo.
 */
function setupLogoHoverAnimation() {
  const logos = document.querySelectorAll(".logo-container");
  logos.forEach((logo) => {
    const link = logo.querySelector("a");
    if (!link) return;
    logo.addEventListener("mouseenter", () =>
      anime({ targets: link, scale: 1.05, duration: 300, easing: "easeOutExpo" })
    );
    logo.addEventListener("mouseleave", () =>
      anime({ targets: link, scale: 1, duration: 300, easing: "easeOutExpo" })
    );
  });
}

/**
 * Sets up the theme switcher to handle clicks on the theme toggle buttons.
 */
function setupThemeSwitcher() {
  const buttons = document.querySelectorAll("#theme-toggle, #theme-toggle-mobile");
  const html = document.documentElement;

  const updateTheme = (isDark) => {
    html.classList.toggle("dark", isDark);
    buttons.forEach((btn) => {
      const icon = btn.querySelector("span");
      if (icon) icon.textContent = isDark ? "dark_mode" : "light_mode";
    });
    localStorage.setItem("theme", isDark ? "dark" : "light");
  };

  const stored = localStorage.getItem("theme");
  updateTheme(stored === "dark");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const isDark = html.classList.contains("dark");
      updateTheme(!isDark);
    });
  });
}

// =================================================================================================
// 🚀 Initialisation globale
// =================================================================================================

document.addEventListener("DOMContentLoaded", () => {
  setupThemeSwitcher();
  setupLanguageSwitcher();
  setLanguage("fr");
  initializeWebsiteInteractivity();
});
