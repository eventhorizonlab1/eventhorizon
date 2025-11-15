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

- [User Guide](#user-guide)
- [Getting Started](#getting-started)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [JavaScript Documentation](#javascript-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Project Analysis](#project-analysis)

## User Guide

### Navigation
- **Smooth Scrolling**: Clicking on a navigation link will smoothly scroll to the corresponding section.
- **Dark Mode**: Click the sun/moon icon in the header to toggle between light and dark mode.
- **Language Switching**: Switch between French and English by clicking the "FR" or "EN" links in the header.

### Carousels
- **Mouse**: Click and drag to scroll through the carousels.
- **Keyboard**: Use the left and right arrow keys to navigate, and the "Home" and "End" keys to jump to the beginning or end.
- **Touch**: Swipe left and right to scroll.

### Black Hole Simulation
- **Rotation**: Click and drag to rotate the black hole.
- **Zoom**: Use the mouse wheel to zoom in and out.
- **Controls**: A control panel is available in the top-left corner to adjust the simulation parameters.

## Technology Stack

The website is built with a simple and robust technology stack:

-   **HTML**: The core markup for all pages.
-   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
-   **Alpine.js**: A minimal JavaScript framework for adding interactivity.
-   **anime.js**: A lightweight JavaScript animation library.

All external libraries are loaded via CDN links in the HTML files, eliminating the need for a complex build process.

## Project Structure

The repository is organized as follows:

-   `index.html`: The main landing page, featuring the latest videos and articles.
-   `locales/`: This directory contains the JSON files for internationalization. `fr.json` and `en.json` hold the translations for French and English, respectively.
-   `documentation.js`: This file contains all JavaScript code for the website, including animations, theme switching, and other interactive features. It is fully documented with JSDoc.
-   `test_*.py`: A suite of Python-based tests to ensure the consistency and correctness of the website.
-   `README.md`: This file, providing a comprehensive overview of the project.

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

You will need to have Python and pip installed to run the tests.

### Installation & Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/event-horizon.git
    ```
2.  **Navigate to the project directory:**
    ```bash
    cd event-horizon
    ```
3.  **Open `index.html` in your web browser to view the site:**
    ```
    # On macOS
    open index.html

    # On Windows
    start index.html

    # On Linux
    xdg-open index.html
    ```

### Running the Tests

To run the tests, you need to install the required Python packages:

```bash
pip install -r requirements.txt
```

You also need to install the Playwright browsers:

```bash
playwright install --with-deps
```

## Testing

The project includes a comprehensive suite of Python-based tests to verify the integrity of the website. The testing strategy combines static analysis and browser-based tests to ensure a high level of quality.

### Testing Strategy

The testing strategy is divided into two main categories:

-   **Static Analysis**: These tests check the code for correctness without running it in a browser. They are used to verify things like the presence of required HTML elements, the correctness of links, and the absence of calls to undefined functions.
-   **Browser-based Tests**: These tests use a real browser to simulate user interactions and verify that the website behaves as expected. They are used to test things like animations, language switching, and other interactive features.

This combination of static analysis and browser-based tests provides a high level of confidence in the quality and correctness of the code.

### Running All Tests

To run all tests, execute the following command in your terminal:

```bash
python3 -m unittest discover -p "test_*.py"
```

### Individual Test Suites

You can also run each test file individually:

-   `test_all.py`: Verifies the consistency of shared elements across all HTML pages.
-   `test_footer_links.py`: Verifies that the footer links are correct.
-   `test_social_media_links.py`: Verifies that the social media links are correct.
-   `test_undefined_functions.py`: Verifies that there are no calls to undefined functions in the JavaScript code.

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

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1.  **Fork the repository.**
2.  **Create a new branch** for your feature or bug fix.
3.  **Make your changes** and ensure that all tests pass.
4.  **Submit a pull request** with a clear description of your changes.

## License

This project is licensed under the MIT License.

## Project Analysis

This document provides a comprehensive analysis of the Event Horizon project,
intended to serve as a guide for new developers. It covers the project's
architecture, testing strategy, and other important details.

### Project Architecture

The Event Horizon website is a static website built with a simple and robust
technology stack. This architecture was chosen for its simplicity, performance,
and ease of deployment.

#### Technology Stack

*   **HTML**: The core markup for all pages.
*   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
*   **Alpine.js**: A minimal JavaScript framework for adding interactivity.
*   **anime.js**: A lightweight JavaScript animation library.

All external libraries are loaded via CDN links in the HTML files, eliminating
the need for a complex build process.

#### File Structure

*   `index.html`: The main landing page.
*   `locales/`: Contains JSON files for internationalization.
-   `documentation.js`: The central repository for all JavaScript code.
-   `test_*.py`: A suite of Python-based tests.
-   `README.md`: A high-level overview of the project.
-   `ANALYSIS.md`: This file, providing a deep dive into the project's
    architecture and testing strategy.

### Testing Strategy

The project includes a comprehensive suite of Python-based tests to verify the
integrity of the website. The testing strategy combines static analysis and
browser-based tests to ensure a high level of quality.

#### Static Analysis

These tests check the code for correctness without running it in a browser.
They are used to verify things like the presence of required HTML elements, the
correctness of links, and the absence of calls to undefined functions.

-   `test_all.py`: Verifies the consistency of shared elements.
-   `test_footer_links.py`: Verifies that the footer links are correct.
-   `test_social_media_links.py`: Verifies that the social media links are correct.
-   `test_undefined_functions.py`: Verifies that there are no calls to
    undefined functions in the JavaScript code.

#### Browser-based Tests

These tests use a real browser to simulate user interactions and verify that
the website behaves as expected. They are used to test things like animations,
language switching, and other interactive features.

-   `test_all.py`: Verifies that browser animations and
    interactions work as expected.

This combination of static analysis and browser-based tests provides a high
level of confidence in the quality and correctness of the code.
