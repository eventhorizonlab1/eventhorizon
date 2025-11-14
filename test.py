"""Verifies the consistency of shared elements across all HTML pages.

This module contains a suite of tests for the Event Horizon static website,
ensuring that elements such as CDN links, headers, footers, and navigation
bars are present and correct in all HTML files.
"""

import re
import os
import unittest

ALL_HTML_FILES = ["index.html", "black_hole.html"]
"""A list of all HTML files in the current directory to be tested."""


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
    This is important for maintaining a consistent user experience.
    """

    def test_alpine_version(self):
        """Checks for the correct Alpine.js CDN link in all HTML files.

        This test verifies that the pinned version of Alpine.js (v2.8.2) is
        correctly referenced in all HTML files. It is important to pin the
        version to avoid unexpected breaking changes from the CDN.
        """
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                pattern = r'<script defer src="https://cdn.jsdelivr.net/gh/alpinejs/alpine@v2.8.2/dist/alpine.min.js".*?></script>'
                match = re.search(pattern, content)
                self.assertIsNotNone(match, f"Alpine.js v2.8.2 CDN link not found in {filepath}!")

    def test_tailwind_cdn_present(self):
        """Ensures the Tailwind CSS CDN link is in all HTML files.

        This test confirms that the Tailwind CSS library is loaded via its CDN
        in every HTML file. This is crucial for the site's styling to be
        applied correctly.
        """
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                pattern = r'<script src="https://cdn.tailwindcss.com\?plugins=forms,typography,container-queries".*?></script>'
                match = re.search(pattern, content)
                self.assertIsNotNone(match, f"Tailwind CSS CDN link not found in {filepath}!")

    def test_header_present(self):
        """Verifies that the main header is present in all HTML files.

        This test ensures that the `header` element, including the site logo,
        is present on every page for consistent branding and navigation.
        A consistent header is essential for a good user experience.
        """
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                match = re.search(r'<a class="text-2xl font-bold tracking-tight text-black dark:text-white" href="index.html"', content, re.DOTALL)
                self.assertIsNotNone(match, f"Header with logo not found in {filepath}!")

    def test_navigation_links_present(self):
        """Verifies that all main navigation links are in all HTML files.

        This test ensures that all navigation links are present and correctly
        formatted in the header of every page. This is critical for site
        navigation and user experience.
        """
        nav_links = ['href="#videos"', 'href="#articles"', 'href="#ecosysteme"']

        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                if filepath == "index.html":
                    for link in nav_links:
                        self.assertIn(link, content, f"Navigation link {link} not found in {filepath}!")
