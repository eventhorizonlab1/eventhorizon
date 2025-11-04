# Event Horizon

Event Horizon is a static website for a French-language news source focused on the European space industry. It provides articles, videos, and information about the space ecosystem.

## Technology Stack

The website is built with a simple and robust technology stack:

-   **HTML**: The core markup for all pages.
-   **Tailwind CSS**: A utility-first CSS framework for rapid UI development.
-   **Alpine.js**: A minimal JavaScript framework for adding interactivity.
-   **anime.js**: A lightweight JavaScript animation library.

All external libraries are loaded via CDN links in the HTML files, eliminating the need for a complex build process.

## Project Structure

The repository is organized as follows:

-   `*.html`: The core HTML files for each page of the website (e.g., `index.html`, `articles.html`). Each file is self-contained and can be opened directly in a browser.
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

-   `python3 test.py`: Verifies the consistency of shared elements across all HTML pages (CDN links, headers, footers, etc.).
-   `python3 test_animations.py`: Tests the animation logic to ensure it is correctly implemented.
-   `python3 test_apropos.py`: Contains tests specifically for the 'À propos' page.
-   `python3 test_content.py`: Validates the presence and structure of key content elements.
-   `python3 test_dark_mode.py`: Includes tests for the dark mode functionality.
-   `python3 test_lazy_loading.py`: Contains tests for the lazy loading of images.
-   `python3 test_links.py`: Verifies the integrity of all internal links.

Each test script is self-contained and can be run with `python3 <filename>`. All tests are fully documented with Google Style Python Docstrings.
