"""Tests to validate the content of the Event Horizon website.

This file is fully documented with Google Style Python Docstrings.
"""

import os
import re
import unittest

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

class TestContent(unittest.TestCase):
    """Test suite for website content.

    This class contains tests to ensure that the website content is
    correctly structured and that all expected elements are present.
    """

    def test_animation_targets_present(self):
        """Verifies that animation target classes exist in the HTML.

        This test ensures that the CSS classes used to target animations
        are present in the HTML of the relevant pages.
        """
        for filepath in ['articles.html', 'videos.html', 'articles-en.html', 'videos-en.html']:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                self.assertRegex(content, r'class="[^"]*animate-card[^"]*"', f"Missing .animate-card in {filepath}")

    def test_contact_form_present(self):
        """Ensures the contact form is correctly structured.

        This test verifies that the contact form is present on the contact
        pages and that it contains an email input field.
        """
        for filepath in ['contact.html', 'contact-en.html']:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                self.assertIn('<form', content, f"Missing form in {filepath}")
                self.assertIn('type="email"', content, f"Missing email input in {filepath}")
