# Event Horizon

Event Horizon is a static website for a French-language news source focused on the European space industry. It is built with HTML, Tailwind CSS, and Alpine.js. All external libraries are loaded via CDN links in the HTML files.

## Project Structure

The repository is organized as follows:

- `*.html`: These are the core HTML files for each page of the website (e.g., `index.html`, `articles.html`).
- `animations.js`: This file contains all the JavaScript code for the website's animations, using the `anime.js` library.
- `test.py`: This script contains a suite of tests to ensure the consistency and correctness of the website's shared elements.
- `test_apropos.py`: This script contains tests specifically for the 'À propos' page.
- `README.md`: This file, providing an overview of the project.

## Setup

No complex setup is required to run this project. The website is static and can be run by opening the HTML files directly in a web browser.

## Usage

To view the website, simply open any of the `.html` files in your preferred web browser.

## Testing

The project includes a set of Python-based tests to verify the integrity of the website. To run the tests, execute the following commands in your terminal:

```bash
python3 test.py
python3 test_apropos.py
```

The tests check for the following:
- Correct CDN links for all external libraries (Tailwind CSS, Alpine.js).
- The presence of a consistent header and footer across all pages.
- The existence of all main navigation links.
- The presence of the language switcher.
- Correct links on the 'À propos' page.
