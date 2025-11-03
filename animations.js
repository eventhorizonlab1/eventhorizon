/**
 * @file This file contains the animations for the Event Horizon website, implemented using the anime.js library.
 * @author Jules
 */

document.addEventListener('DOMContentLoaded', () => {
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
     * Animates the cards on the page with a stagger effect.
     * @property {string} targets - The CSS selector for the elements to animate.
     * @property {Array<number>} opacity - The starting and ending opacity.
     * @property {Array<number>} translateY - The starting and ending vertical position.
     * @property {number} duration - The duration of the animation in milliseconds.
     * @property {Function} delay - The delay between each animation.
     * @property {string} ease - The easing function for the animation.
     */
    animate({
        targets: '.animate-card',
        opacity: [0, 1],
        translateY: [20, 0],
        duration: 800,
        delay: stagger(100, { start: 500 }),
        ease: 'easeOutExpo'
    });
});
