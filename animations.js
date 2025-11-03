// Fichier dédié aux animations du site Event Horizon avec anime.js

document.addEventListener('DOMContentLoaded', () => {
    const { animate, stagger } = anime;

    // Animation for titles
    animate({
        targets: '.animate-title',
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        delay: stagger(200, { start: 300 }),
        ease: 'easeOutExpo'
    });

    // Stagger animation for cards
    animate({
        targets: '.animate-card',
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        delay: stagger(100, { start: 500 }),
        ease: 'easeOutExpo'
    });
});
