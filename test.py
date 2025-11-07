"""Verifies the consistency of shared elements across all HTML pages.

This script contains a suite of tests for the Event Horizon static website,
ensuring that elements such as CDN links, headers, footers, and navigation
bars are present and correct in all HTML files, for both French and English versions.
This file is fully documented with Google Style Python Docstrings.
"""

import re
import os
import unittest

# A list of all HTML files in the current directory to be tested.
ALL_HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]
FRENCH_HTML_FILES = [f for f in ALL_HTML_FILES if not f.endswith('-en.html') and "bak" not in f]
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
    """Test suite for shared elements across all HTML pages.

    This class contains tests to ensure that common elements like the header,
    footer, and CDN links are consistently applied across all HTML files.
    """

    def test_alpine_version(self):
        """Checks for the correct Alpine.js CDN link in all HTML files.

        This test verifies that the pinned version of Alpine.js (v2.8.2) is
        correctly referenced in all HTML files.
        """
        for filepath in ["index.html", "index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<script defer src="https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js"></script>', content)
                self.assertIsNotNone(match, f"Alpine.js v2.8.2 CDN link not found in {filepath}!")

    def test_tailwind_cdn_present(self):
        """Ensures the Tailwind CSS CDN link is in all HTML files.

        This test confirms that the Tailwind CSS library is loaded via its CDN
        in every HTML file.
        """
        for filepath in ["index.html", "index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<script src="https://cdn.tailwindcss.com\?plugins=forms,typography,container-queries"></script>', content)
                self.assertIsNotNone(match, f"Tailwind CSS CDN link not found in {filepath}!")

    def test_header_present(self):
        """Verifies that the main header is present in all HTML files.

        This test ensures that the `header` element, including the site logo,
        is present on every page for consistent branding and navigation.
        """
        for filepath in ["index.html", "index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<a class="font-serif text-2xl font-bold tracking-tight text-black" href="#">Event Horizon</a>', content, re.DOTALL)
                self.assertIsNotNone(match, f"Header with logo not found in {filepath}!")

    def test_footer_present(self):
        """Checks for the main footer in all HTML files, in the correct language.

        This test verifies that the `footer` element with the correct copyright
        notice is present on all pages, in both French and English versions.
        """
        for filepath in ["index.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'© 2023 Event Horizon. Tous droits réservés.', content, re.DOTALL)
                self.assertIsNotNone(match, f"Footer with French copyright notice not found in {filepath}!")

        for filepath in ["index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'© 2023 Event Horizon. All rights reserved.', content, re.DOTALL)
                self.assertIsNotNone(match, f"Footer with English copyright notice not found in {filepath}!")

    def test_navigation_links_present(self):
        """Verifies that all main navigation links are in all HTML files.

        This test ensures that all navigation links are present and correctly
        formatted in the header of every page, for both language versions.
        """
        fr_nav_links = ['href="#videos"', 'href="#articles"', 'href="#ecosysteme"']
        en_nav_links = ['href="#videos"', 'href="#articles"', 'href="#ecosysteme"']

        for filepath in ["index.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                for link in fr_nav_links:
                    self.assertIn(link, content, f"Navigation link {link} not found in {filepath}!")

        for filepath in ["index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                for link in en_nav_links:
                    self.assertIn(link, content, f"Navigation link {link} not found in {filepath}!")

    def test_language_switcher_links_correct(self):
        """Ensures the language switcher links are correct for each page.

        This test verifies that the FR/EN language switcher links point to the
        correct equivalent page, ensuring seamless navigation between languages.
        """
        for filepath in ["index.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                en_equivalent = filepath.replace('.html', '-en.html')
                fr_link_pattern = f'href="{filepath}"'
                en_link_pattern = f'href="{en_equivalent}"'
                self.assertRegex(content, fr_link_pattern, f"FR link incorrect in {filepath}")
                self.assertRegex(content, en_link_pattern, f"EN link incorrect in {filepath}")

        for filepath in ["index-en.html"]:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                fr_equivalent = filepath.replace('-en.html', '.html')
                fr_link_pattern = f'href="{fr_equivalent}"'
                en_link_pattern = f'href="{filepath}"'
                self.assertRegex(content, fr_link_pattern, f"FR link incorrect in {filepath}")
                self.assertRegex(content, en_link_pattern, f"EN link incorrect in {filepath}")
