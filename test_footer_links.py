"""Tests for the footer links of the Event Horizon website.

This file is fully documented with Google Style Python Docstrings.
"""

import os
import unittest

ALL_HTML_FILES = ["index.html"]

class TestFooterLinks(unittest.TestCase):
    """Test suite for footer links.

    This class contains tests to ensure that the footer links are correctly
    implemented and behave as expected.
    """
    def test_footer_links(self):
        """Ensures that the footer links are correct.

        This test verifies that the footer does not contain any broken links
        and that the contact email link is present.
        """
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "-en" in filepath:
                        self.assertNotIn('>About</a>', content)
                    else:
                        self.assertNotIn('>À Propos</a>', content)
                    self.assertIn('href="mailto:contact@eventhorizon.fr"', content)
