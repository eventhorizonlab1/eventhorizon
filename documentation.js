/**
 * Event Horizon - Interactive Script (version ultime)
 * Effet réseau de particules connectées, pulsantes, réactives au curseur et au scroll
 */

let translations = {};

// ================================================================
// 🌍 Gestion des langues
// ================================================================
async function loadTranslations(lang) {
  try {
    const response = await fetch(`locales/${lang}.json`);
    if (!response.ok) throw new Error(`Network response was not ok for ${lang}.json`);
    translations = await response.json();
  } catch (error) {
    console.error("Failed to load translations:", error);
  }
}

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

async function setLanguage(lang) {
  await loadTranslations(lang);
  applyTranslations();
  updateLanguageSwitcherUI(lang);
}

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
// ✨ ANIMATIONS & INTERACTIVITÉ
// ================================================================
function initializeWebsiteInteractivity() {
  anime.timeline({ easing: "easeOutExpo", duration: 1000 })
    .add(animateHeader())
    .add(animateMainTitle(), "-=500");

  setupIntersectionObserver();
  setupQuickLinkHovers();
  setupLogoHoverAnimation();
  setupHoverAnimations();
  animateSectionTitles();

  // 🌌 Fond spatial animé
  initializeParticleNetwork();
}

// ================================================================
// 🌌 Réseau de particules connectées : pulsation + curseur + scroll
// ================================================================
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

  function resizeCanvas() {
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
  }
  window.addEventListener("resize", resizeCanvas);
  resizeCanvas();

  // 🧭 Curseur
  window.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    mouse.x = e.clientX - rect.left;
    mouse.y = e.clientY - rect.top;
  });
  window.addEventListener("mouseleave", () => {
    mouse.x = null;
    mouse.y = null;
  });

  // 🌀 Scroll reactivity
  let lastScroll = window.scrollY;
  window.addEventListener("scroll", () => {
    const delta = window.scrollY - lastScroll;
    scrollOffset = anime.utils.clamp(-1, 1, delta * 0.02);
    lastScroll = window.scrollY;
  });

  // Particules initiales
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

  function drawNetwork() {
    const isDark = document.documentElement.classList.contains("dark");
    const dotColor = isDark ? "rgba(255,255,255,0.7)" : "rgba(0,0,0,0.6)";
    const baseLineColor = isDark ? "255,255,255" : "0,0,0";

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let p of particles) {
      p.x += p.vx + scrollOffset * 0.5; // effet scroll
      p.y += p.vy - scrollOffset * 0.3;

      if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.vy *= -1;

      // Interaction curseur
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

      // Pulsation (respiration lumineuse)
      p.pulse += 0.02;
      const pulseScale = 1 + Math.sin(p.pulse) * 0.3;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.radius * pulseScale, 0, Math.PI * 2);
      ctx.fillStyle = dotColor;
      ctx.fill();
    }

    pulseTime += 0.02;
    const pulseIntensity = (Math.sin(pulseTime) + 1) / 2;

    // Connexions
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

    // Dissipation progressive du scrollOffset
    scrollOffset *= 0.9;

    requestAnimationFrame(drawNetwork);
  }

  // Apparition douce
  anime({
    targets: particles,
    opacity: [0, 1],
    easing: "easeOutSine",
    duration: 1000,
    complete: drawNetwork,
  });
}

// ================================================================
// Autres animations
// ================================================================
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

// ================================================================
// 🚀 Initialisation
// ================================================================
document.addEventListener("DOMContentLoaded", () => {
  setupThemeSwitcher();
  setupLanguageSwitcher();
  setLanguage("fr");
  initializeWebsiteInteractivity();
});
