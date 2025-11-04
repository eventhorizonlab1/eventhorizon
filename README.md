# Event Horizon

Event Horizon is a static website for a French-language news source focused on the European space industry. It is built with HTML, Tailwind CSS, and Alpine.js. All external libraries are loaded via CDN links in the HTML files.

## Project Structure

The repository is organized as follows:

-   `*.html`: These are the core HTML files for each page of the website (e.g., `index.html`, `articles.html`).
-   `documentation.js`: This file contains all the JavaScript code for the website's animations and theme switching, with JSDoc documentation.
-   `test_*.py`: A suite of Python-based tests to ensure the consistency and correctness of the website.
-   `README.md`: This file, providing an overview of the project.

## Setup

No complex setup is required to run this project. The website is static and can be run by opening the HTML files directly in a web browser.

## Usage

To view the website, simply open any of the `.html` files in your preferred web browser.

## Testing

The project includes a set of Python-based tests to verify the integrity of the website. The tests are organized as follows:

-   `test.py`: Verifies the consistency of shared elements across all HTML pages (CDN links, headers, footers, etc.).
-   `test_animations.py`: Tests the animation logic.
-   `test_apropos.py`: Contains tests specifically for the 'À propos' page.
-   `test_content.py`: Validates the content of the website.
-   `test_links.py`: Verifies the integrity of internal links.

To run all tests, execute the following command in your terminal:

```bash
python3 -m unittest discover -p "test_*.py"
```

Alternatively, you can run each test file individually:

```bash
python3 test.py
python3 test_animations.py
python3 test_apropos.py
python3 test_content.py
python3 test_links.py
```
