"""Tests specifically for the 'À propos' page.

Verifies that all navigation links pointing to the 'À propos' page
are correctly formatted. This file is fully documented with
Google Style Python Docstrings.
"""

import re
import os
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

class TestAProposPage(unittest.TestCase):
    """Test suite for the 'À propos' page.

    This class contains tests to ensure that the 'À propos' and 'About' pages
    have the correct links and content.
    """

    def test_apropos_links(self):
        """Checks that all links to 'À propos' on its own page are correct.

        This test verifies that all navigation links pointing to the
        'À propos' page are correctly formatted.
        """
        content = read_file_content('a-propos.html')

        # Find all 'À propos' links
        matches = re.findall(r'<a[^>]*>À Propos</a>', content)

        # Check that there are at least two such links (header and footer)
        self.assertGreaterEqual(len(matches), 2, "Expected at least two 'À propos' links in a-propos.html")

        # Check that all 'À propos' links have the correct href
        for match in matches:
            with self.subTest(match=match):
                self.assertIn('href="a-propos.html"', match, f"Incorrect 'À propos' link found: {match}")

    def test_about_links(self):
        """Checks that all links to 'About' on its own page are correct.

        This test verifies that all navigation links pointing to the
        'About' page are correctly formatted.
        """
        content = read_file_content('a-propos-en.html')

        # Find all 'About' links
        matches = re.findall(r'<a[^>]*>About</a>', content)

        # Check that there are at least two such links (header and footer)
        self.assertGreaterEqual(len(matches), 2, "Expected at least two 'About' links in a-propos-en.html")

        # Check that all 'About' links have the correct href
        for match in matches:
            with self.subTest(match=match):
                self.assertIn('href="a-propos-en.html"', match, f"Incorrect 'About' link found: {match}")
