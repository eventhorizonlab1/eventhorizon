/**
 * @file This file contains the animations for the Event Horizon website, implemented using the anime.js library.
 * @author Jules
 */

document.addEventListener('DOMContentLoaded', () => {
    // anime is available globally from the script tag

    /**
     * 🎬 Animation du titre principal (<h1>)
     * Au chargement de la page, il apparaît avec un effet fade + slide vers le bas.
     */
    anime({
        targets: '.main-title',
        opacity: [0, 1],
        translateY: [-50, 0],
        duration: 1000,
        ease: 'easeOutExpo'
    });

    /**
     * 🎨 Animation du menu
     * Chaque élément du menu (.menu-item) glisse de la gauche vers sa position d’origine
     * avec un petit délai entre chaque (effet stagger).
     */
    anime({
        targets: '.menu-item',
        opacity: [0, 1],
        translateX: [-50, 0],
        duration: 800,
        delay: anime.stagger(100),
        ease: 'easeOutExpo'
    });

    /**
     * 🪄 Animation des sections
     * Les sections “Dernières vidéos” et “Derniers articles” apparaissent avec un
     * effet fade + slide up lorsqu’elles entrent dans le champ de vision de l’utilisateur.
     */
    const sections = document.querySelectorAll('.animate-section');

    // On prépare les sections en les rendant invisibles et en les décalant vers le bas
    anime.set(sections, {
        opacity: 0,
        translateY: 50
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                anime({
                    targets: entry.target,
                    opacity: 1,
                    translateY: 0,
                    duration: 1000,
                    ease: 'easeOutExpo'
                });
                // On arrête d'observer l'élément une fois qu'il a été animé
                observer.unobserve(entry.target);
            }
        });
    }, {
        // L'animation se déclenche quand 10% de l'élément est visible
        threshold: 0.1
    });

    sections.forEach(section => {
        observer.observe(section);
    });

    /**
     * 💡 Effet hover sur les liens rapides
     * Quand on survole un lien rapide, il doit légèrement monter (translateY -5px)
     * et changer de couleur progressivement.
     */
    const quickLinks = document.querySelectorAll('.quick-link');

    quickLinks.forEach(link => {
        link.addEventListener('mouseenter', () => {
            anime({
                targets: link,
                translateY: -5,
                color: '#06ccf9', // La couleur primaire du site
                duration: 300,
                ease: 'easeOutExpo'
            });
        });

        link.addEventListener('mouseleave', () => {
            anime({
                targets: link,
                translateY: 0,
                duration: 300,
                ease: 'easeOutExpo'
            });
        });
    });

    /**
     * 🌟 Effet "glow" sur le bouton de thème
     * Ajoute un effet de "glow" au survol du bouton de changement de thème.
     */
    const themeToggleButton = document.getElementById('theme-toggle');
    if (themeToggleButton) {
        themeToggleButton.addEventListener('mouseenter', () => {
            anime({
                targets: themeToggleButton,
                boxShadow: '0 0 12px #06ccf9',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });

        themeToggleButton.addEventListener('mouseleave', () => {
            anime({
                targets: themeToggleButton,
                boxShadow: '0 0 0 rgba(0,0,0,0)',
                duration: 300,
                easing: 'easeOutExpo'
            });
        });
    }
});
