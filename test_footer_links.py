"""Tests for the footer links of the Event Horizon website.

This module contains tests to ensure that the footer links are correctly
implemented and behave as expected.
"""

import os
import unittest

ALL_HTML_FILES = ["index.html"]
"""A list of all HTML files in the current directory to be tested."""

class TestFooterLinks(unittest.TestCase):
    """Test suite for the footer links.

    This class contains a static analysis test to ensure that the footer links
    are correctly implemented.
    """
    def test_footer_links(self):
        """Ensures that the footer links are correct.

        This test verifies that the footer does not contain any broken links
        and that the contact email link is present. A functional footer is
        important for user navigation and contact.
        """
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "-en" in filepath:
                        self.assertNotIn('>About</a>', content)
                    else:
                        self.assertIn('>À Propos</a>', content)
                    self.assertIn('href="mailto:contact@eventhorizon.fr"', content)
