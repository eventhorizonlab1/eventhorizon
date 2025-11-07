# Event Horizon

Event Horizon is a static website for a French-language news source focused on the European space industry. It provides articles, videos, and information about the space ecosystem, with a parallel English version available for all pages.

## Purpose

This repository serves as a showcase of a modern, static website that is fully documented and tested. It demonstrates best practices in web development, including:

-   **Responsive Design**: The website is fully responsive and works on all screen sizes, from mobile to desktop.
-   **Bilingual Support**: All content is available in both French and English, with a seamless language switcher.
-   **Animations and Interactivity**: The website uses JavaScript to create a dynamic and engaging user experience.
-   **Testing**: A comprehensive suite of tests is included to ensure the quality and correctness of the code.
-   **Documentation**: The entire codebase, including JavaScript and Python files, is fully documented.

## Table of Contents

- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Setup and Usage](#setup-and-usage)
- [Testing](#testing)
- [JavaScript Documentation](#javascript-documentation)
- [License](#license)

## Technology Stack

The website is built with a simple and robust technology stack:

-   **HTML**: The core markup for all pages.
-   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
-   **Alpine.js**: A minimal JavaScript framework for adding interactivity.
-   **anime.js**: A lightweight JavaScript animation library.

All external libraries are loaded via CDN links in the HTML files, eliminating the need for a complex build process.

## Project Structure

The repository is organized as follows:

-   `index.html` / `index-en.html`: The main landing page, featuring the latest videos and articles.
-   `videos.html` / `videos-en.html`: A gallery of all video content.
-   `articles.html` / `articles-en.html`: A collection of all written articles.
-   `ecosysteme.html` / `ecosysteme-en.html`: Information about the European space ecosystem.
-   `a-propos.html` / `a-propos-en.html`: The "About" page, with information about the project and its creator.
-   `contact.html` / `contact-en.html`: A contact page with a form for user inquiries.
-   `documentation.js`: This file contains all JavaScript code for the website, including animations, theme switching, and other interactive features. It is fully documented with JSDoc.
-   `test_*.py`: A suite of Python-based tests to ensure the consistency and correctness of the website.
-   `README.md`: This file, providing a comprehensive overview of the project.

## Setup and Usage

No complex setup is required to run this project. The website is static and can be run by following these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/event-horizon.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd event-horizon
    ```
3.  **Open any `.html` file in your web browser:**
    ```
    # On macOS
    open index.html

    # On Windows
    start index.html

    # On Linux
    xdg-open index.html
    ```

## Testing

The project includes a comprehensive suite of Python-based tests to verify the integrity of the website. These tests are designed to be run without any additional setup.

### Running All Tests

To run all tests, execute the following command in your terminal:

```bash
python3 -m unittest discover -p "test_*.py"
```

### Individual Test Suites

You can also run each test file individually:

-   `test.py`: Verifies the consistency of shared elements across all HTML pages, such as CDN links, headers, footers, and navigation links.
-   `test_animations.py`: Tests the animation logic in `documentation.js` to ensure that animations are correctly implemented and behave as expected.
-   `test_apropos.py`: Contains tests specifically for the 'À propos' and 'About' pages, checking for correct links and content.
-   `test_content.py`: Validates the presence and structure of key content elements, such as animation targets and contact forms, across the relevant pages.
-   `test_dark_mode.py`: Includes tests for the dark mode functionality, ensuring that theme-dependent features are correctly implemented.
-   `test_lazy_loading.py`: Contains tests for the lazy loading of images, verifying that the correct attributes and classes are present.
-   `test_links.py`: Verifies the integrity of all internal links to prevent broken navigation.
-   `test_browser_animations.py`: Uses Playwright to simulate user interactions and verify that the JavaScript-based animations behave as expected in a live browser environment.
-   `test_browser_documentation.py`: Uses Playwright to simulate user interactions and verify that the JavaScript functions in `documentation.js` are behaving as expected.
-   `test_hardcoded_hover_color.py`: Verifies that the quick link hover animation does not use a hardcoded color, which would cause issues when the theme is changed.
-   `test_link_checker_logic.py`: Verifies that there is no redundant link check logic in `test_links.py`, ensuring that the test logic is clean and maintainable.
-   `test_quick_link_theme_change.py`: Verifies that the quick link hover animation does not use a hardcoded color, which would cause issues when the theme is changed.


Each test script is self-contained and can be run with `python3 <filename>`. All tests are fully documented with Google Style Python Docstrings.

## JavaScript Documentation

All JavaScript code is located in the `documentation.js` file and is fully documented using JSDoc. This allows for the automatic generation of a documentation website, making it easy to understand the purpose and functionality of each JavaScript function.

### Generating Documentation

1.  **Install JSDoc:**
    ```bash
    npm install -g jsdoc
    ```
2.  **Generate the documentation:**
    ```bash
    jsdoc documentation.js
    ```
This will create an `out` directory containing the HTML documentation.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
