"""Verifies the consistency of shared elements across all HTML pages.

This script contains a suite of tests for the Event Horizon static website,
ensuring that elements such as CDN links, headers, footers, and navigation
bars are present and correct in all HTML files.
"""

import re
import os

# A list of all HTML files in the current directory to be tested.
HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def test_alpine_version():
    """Checks for the correct Alpine.js CDN link in all HTML files.

    Raises:
        AssertionError: If the expected CDN link is not found.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<script defer src="https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js"></script>', content)
        assert match is not None, f"Alpine.js v2.8.2 CDN link not found in {filepath}!"

def test_tailwind_cdn_present():
    """Ensures the Tailwind CSS CDN link is in all HTML files.

    Raises:
        AssertionError: If the Tailwind CSS CDN link is missing.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<script src="https://cdn.tailwindcss.com"></script>', content)
        assert match is not None, f"Tailwind CSS CDN link not found in {filepath}!"

def test_header_present():
    """Verifies that the main header is present in all HTML files.

    Raises:
        AssertionError: If the header with the site logo is not found.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<header.*>.*<h2.*>Event Horizon</h2>.*</header>', content, re.DOTALL)
        assert match is not None, f"Header with logo not found in {filepath}!"

def test_footer_present():
    """Checks for the main footer in all HTML files.

    Raises:
        AssertionError: If the footer with the copyright notice is missing.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<footer.*>.*© 2024 Event Horizon. Tous droits réservés..*</footer>', content, re.DOTALL)
        assert match is not None, f"Footer with copyright notice not found in {filepath}!"

def test_navigation_links_present():
    """Verifies that all main navigation links are in all HTML files.

    Raises:
        AssertionError: If any expected navigation links are missing.
    """
    nav_links = [
        'href="index.html"',
        'href="videos.html"',
        'href="articles.html"',
        'href="ecosysteme.html"',
        'href="a-propos.html"',
        'href="contact.html"'
    ]
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        for link in nav_links:
            assert link in content, f"Navigation link {link} not found in {filepath}!"

def test_language_switcher_present():
    """Ensures the language switcher is present in all HTML files.

    Raises:
        AssertionError: If the FR/EN language switcher is not found.
    """
    for filepath in HTML_FILES:
        content = read_file_content(filepath)
        match = re.search(r'<a class="text-gray-800 dark:text-white px-2 py-1 rounded-md" href="#">FR</a>', content)
        assert match is not None, f"Language switcher not found in {filepath}!"

if __name__ == "__main__":
    # Run all tests
    test_alpine_version()
    print("Test passed: Alpine.js CDN link is correct in all files.")
    test_tailwind_cdn_present()
    print("Test passed: Tailwind CSS CDN link is present in all files.")
    test_header_present()
    print("Test passed: Header is present in all files.")
    test_footer_present()
    print("Test passed: Footer is present in all files.")
    test_navigation_links_present()
    print("Test passed: Navigation links are present in all files.")
    test_language_switcher_present()
    print("Test passed: Language switcher is present in all files.")

    print("\nAll tests passed successfully!")
