/**
 * @file This script handles all the interactive elements of the Event Horizon website.
 * @description It includes functionality for language switching, animations, and theme management.
 * @version 1.0.0
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
    if (!response.ok) throw new Error(`Network response was not ok for ${lang}.json`);
    translations = await response.json();
  } catch (error) {
    console.error("Failed to load translations:", error);
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
  await loadTranslations(lang);
  applyTranslations();
  updateLanguageSwitcherUI(lang);
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
// ✨ ANIMATIONS & INTERACTIVITY
// ================================================================

/**
 * Initializes all the main animations and interactive features of the website.
 *
 * @description This function serves as the entry point for all visual effects, including
 * the header and main title animations, intersection observers for scroll
 * animations, and various hover effects. It also initializes the animated
 * particle network in the background.
 *
 * @returns {void}
 */
function initializeWebsiteInteractivity() {
  anime.timeline({ easing: "easeOutExpo", duration: 1000 })
    .add(animateHeader())
    .add(animateMainTitle(), "-=500");

  setupIntersectionObserver();
  setupQuickLinkHovers();
  setupLogoHoverAnimation();
  setupHoverAnimations();
  animateSectionTitles();

  initializeParticleNetwork();
}

/**
 * Initializes and manages the animated particle network background.
 *
 * @description This function creates a canvas element and draws a network of particles
 * that are connected by lines. The particles pulse, react to the cursor,
 * and respond to scroll events. It is a major visual feature of the site.
 *
 * @returns {void}
 */
function initializeParticleNetwork() {
  const container = document.getElementById("particle-container");
  if (!container) return;

  const canvas = document.createElement("canvas");
  canvas.id = "particle-network";
  canvas.style.position = "absolute";
  canvas.style.inset = "0";
  canvas.style.zIndex = "-1";
  canvas.style.width = "100%";
  canvas.style.height = "100%";
  container.innerHTML = "";
  container.appendChild(canvas);

  const ctx = canvas.getContext("2d");
  let particles = [];
  const numParticles = 80;
  const maxDist = 160;

  let mouse = { x: null, y: null, radius: 200 };
  let scrollOffset = 0;

  /**
   * Resizes the canvas to match the dimensions of its container.
   * @returns {void}
   */
  function resizeCanvas() {
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  window.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  window.addEventListener("mouseleave", () => {
    mouse.x = null;
    mouse.y = null;
  });

  let lastScroll = window.scrollY;
  window.addEventListener("scroll", () => {
    const delta = window.scrollY - lastScroll;
    scrollOffset = anime.utils.clamp(-1, 1, delta * 0.02);
    lastScroll = window.scrollY;
  });

  for (let i = 0; i < numParticles; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.6,
      vy: (Math.random() - 0.5) * 0.6,
      radius: Math.random() * 2 + 1,
      pulse: Math.random() * Math.PI * 2,
    });
  }

  let pulseTime = 0;

  /**
   * Draws the particle network on the canvas.
   * @description This function is the core of the particle animation, responsible for
   * updating particle positions, handling interactions, and drawing the
   * particles and their connections. It is called on every frame.
   * @returns {void}
   */
  function drawNetwork() {
    const isDark = document.documentElement.classList.contains("dark");
    const dotColor = isDark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.6)";
    const baseLineColor = isDark ? "255,255,255" : "0,0,0";

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let p of particles) {
      p.x += p.vx + scrollOffset * 0.5;
      p.y += p.vy - scrollOffset * 0.3;

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      if (mouse.x && mouse.y) {
        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < mouse.radius) {
          const force = (mouse.radius - dist) / mouse.radius;
          p.vx -= (dx / dist) * force * 0.03;
          p.vy -= (dy / dist) * force * 0.03;
        }
      }

      p.pulse += 0.02;
      const pulseScale = 1 + Math.sin(p.pulse) * 0.3;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius * pulseScale, 0, Math.PI * 2);
      ctx.fillStyle = dotColor;
      ctx.fill();
    }

    pulseTime += 0.02;
    const pulseIntensity = (Math.sin(pulseTime) + 1) / 2;

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < maxDist) {
          const alpha = (1 - dist / maxDist) * (0.2 + pulseIntensity * 0.3);
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = `rgba(${baseLineColor}, ${alpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    scrollOffset *= 0.9;

    requestAnimationFrame(drawNetwork);
  }

  anime({
    targets: particles,
    opacity: [0, 1],
    easing: "easeOutSine",
    duration: 1000,
    complete: drawNetwork,
  });
}

// ================================================================
// Other Animations
// ================================================================

/**
 * Animates the main title of the page with a staggered word effect.
 *
 * @description This function splits the main title into individual words, wraps each in a
 * `<span>`, and then uses `anime.js` to animate them into view with a staggered
 * delay. This creates a dramatic entrance effect.
 *
 * @returns {anime.AnimeInstance | undefined} An anime.js animation instance, or undefined if the main title is not found.
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
 * Animates the navigation elements in the header.
 *
 * @description This function uses `anime.js` to animate the opacity and position of the
 * navigation links, creating a smooth fade-in and slide-down effect when the
 * page loads.
 *
 * @returns {anime.AnimeInstance} An anime.js animation instance.
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
 * Sets up an Intersection Observer to trigger animations on scroll.
 *
 * @description This function observes sections of the page and, when they become visible
 * in the viewport, triggers a fade-in and slide-up animation for the elements
 * within them. This creates a dynamic and engaging experience as the user
 * scrolls down the page.
 *
 * @returns {void}
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
  sections.forEach((s) => observer.observe(s));
}

/**
 * Animates all section titles with a fade-in and slide-up effect.
 *
 * @description This function targets all `<h2>` elements within `<section>` tags and uses
 * `anime.js` to animate them into view. This helps to draw attention to the
 * different sections of the page.
 *
 * @returns {void}
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
 * Sets up hover animations for the quick links in the footer.
 *
 * @description This function attaches `mouseenter` and `mouseleave` event listeners to the
 * quick links, creating a subtle animation effect when the user hovers over
 * them. The animation is theme-aware and adjusts accordingly.
 *
 * @returns {void}
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
 * Sets up generic hover animations for various interactive elements.
 *
 * @description This function applies a subtle scaling effect to buttons, article cards,
 * and other designated elements when the user hovers over them. This provides
 * visual feedback and enhances the user experience.
 *
 * @returns {void}
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

 * Sets up a hover animation for the site logo.
 *
 * @description This function applies a subtle scaling effect to the logo when the user
 * hovers over it, providing visual feedback and enhancing the user experience.
 *
 * @returns {void}
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
 * Sets up the theme switcher functionality.
 *
 * @description This function initializes the theme based on the user's `localStorage`
 * preference and attaches click event listeners to the theme toggle buttons.
 * It also handles updating the UI and persisting the theme choice.
 *
 * @returns {void}
 */
function setupThemeSwitcher() {
  const buttons = document.querySelectorAll("#theme-toggle, #theme-toggle-mobile");
  const html = document.documentElement;

  /**
   * Updates the theme of the website.
   * @param {boolean} isDark - A boolean indicating whether to apply the dark theme.
   * @returns {void}
   */
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

// ================================================================
// 🚀 Initialization
// ================================================================
document.addEventListener("DOMContentLoaded", () => {
  setupThemeSwitcher();
  setupLanguageSwitcher();
  setLanguage("fr");

  // Only run the main page animations if we're on a page that has the particle container
  if (document.getElementById("particle-container")) {
    initializeWebsiteInteractivity();
  }
});
