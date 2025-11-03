/**
 * @file This file contains the animations for the Event Horizon website, implemented using the anime.js library.
 * @author Jules
 */

document.addEventListener('DOMContentLoaded', () => {
    // anime is available globally from the script tag
    const { animate, stagger } = anime;

    /**
     * Animates the titles on the page.
     * @property {string} targets - The CSS selector for the elements to animate.
     * @property {Array<number>} opacity - The starting and ending opacity.
     * @property {Array<number>} translateY - The starting and ending vertical position.
     * @property {number} duration - The duration of the animation in milliseconds.
     * @property {Function} delay - The delay between each animation.
     * @property {string} ease - The easing function for the animation.
     */
    animate({
        targets: '.animate-title',
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        delay: stagger(200, { start: 300 }),
        ease: 'easeOutExpo'
    });

    /**
     * Animates the cards on the page when they scroll into view.
     */
    const cards = document.querySelectorAll('.animate-card');

    // Set initial styles for animation
    anime.set(cards, {
        opacity: 0,
        translateY: 20
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animate({
                    targets: entry.target,
                    opacity: 1,
                    translateY: 0,
                    duration: 800,
                    ease: 'easeOutExpo'
                });
                // Stop observing the element after it has been animated
                observer.unobserve(entry.target);
            }
        });
    }, {
        // Start loading the animation when the element is 10% visible
        threshold: 0.1
    });

    cards.forEach(card => {
        observer.observe(card);
    });
});
