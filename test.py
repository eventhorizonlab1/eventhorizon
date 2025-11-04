"""Verifies the consistency of shared elements across all HTML pages.

This script contains a suite of tests for the Event Horizon static website,
ensuring that elements such as CDN links, headers, footers, and navigation
bars are present and correct in all HTML files, for both French and English versions.
"""

import re
import os
import unittest

# A list of all HTML files in the current directory to be tested.
ALL_HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]
FRENCH_HTML_FILES = [f for f in ALL_HTML_FILES if not f.endswith('-en.html')]
ENGLISH_HTML_FILES = [f for f in ALL_HTML_FILES if f.endswith('-en.html')]

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestSharedElements(unittest.TestCase):
    """Test suite for shared elements across all HTML pages."""

    def test_alpine_version(self):
        """Checks for the correct Alpine.js CDN link in all HTML files."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<script defer src="https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js"></script>', content)
                self.assertIsNotNone(match, f"Alpine.js v2.8.2 CDN link not found in {filepath}!")

    def test_tailwind_cdn_present(self):
        """Ensures the Tailwind CSS CDN link is in all HTML files."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<script src="https://cdn.tailwindcss.com"></script>', content)
                self.assertIsNotNone(match, f"Tailwind CSS CDN link not found in {filepath}!")

    def test_header_present(self):
        """Verifies that the main header is present in all HTML files."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<header.*>.*<h2.*>Event Horizon</h2>.*</header>', content, re.DOTALL)
                self.assertIsNotNone(match, f"Header with logo not found in {filepath}!")

    def test_footer_present(self):
        """Checks for the main footer in all HTML files, in the correct language."""
        for filepath in FRENCH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<footer.*>.*© 2024 Event Horizon. Tous droits réservés..*</footer>', content, re.DOTALL)
                self.assertIsNotNone(match, f"French footer with copyright notice not found in {filepath}!")

        for filepath in ENGLISH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<footer.*>.*© 2024 Event Horizon. All rights reserved..*</footer>', content, re.DOTALL)
                self.assertIsNotNone(match, f"English footer with copyright notice not found in {filepath}!")

    def test_navigation_links_present(self):
        """Verifies that all main navigation links are in all HTML files."""
        fr_nav_links = ['href="index.html"', 'href="videos.html"', 'href="articles.html"', 'href="ecosysteme.html"', 'href="a-propos.html"', 'href="contact.html"']
        en_nav_links = ['href="index-en.html"', 'href="videos-en.html"', 'href="articles-en.html"', 'href="ecosysteme-en.html"', 'href="a-propos-en.html"', 'href="contact-en.html"']

        for filepath in FRENCH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                for link in fr_nav_links:
                    self.assertIn(link, content, f"Navigation link {link} not found in {filepath}!")

        for filepath in ENGLISH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                for link in en_nav_links:
                    self.assertIn(link, content, f"Navigation link {link} not found in {filepath}!")

    def test_language_switcher_links_correct(self):
        """Ensures the language switcher links are correct for each page."""
        for filepath in FRENCH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                en_equivalent = filepath.replace('.html', '-en.html')
                fr_link_pattern = f'href="{filepath}"'
                en_link_pattern = f'href="{en_equivalent}"'
                self.assertRegex(content, fr_link_pattern, f"FR link incorrect in {filepath}")
                self.assertRegex(content, en_link_pattern, f"EN link incorrect in {filepath}")

        for filepath in ENGLISH_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                fr_equivalent = filepath.replace('-en.html', '.html')
                fr_link_pattern = f'href="{fr_equivalent}"'
                en_link_pattern = f'href="{filepath}"'
                self.assertRegex(content, fr_link_pattern, f"FR link incorrect in {filepath}")
                self.assertRegex(content, en_link_pattern, f"EN link incorrect in {filepath}")
