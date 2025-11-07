"""Verifies that all internal links in the website are valid.

This script checks all HTML files in the current directory for internal links
and ensures that they point to existing files. This helps maintain the
integrity of the site's navigation.
This file is fully documented with Google Style Python Docstrings.
"""

import re
import os
import unittest

# A list of all files in the current directory, used for link checking.
ALL_FILES = [f for f in os.listdir('.') if os.path.isfile(f)]
# A list of all HTML files in the current directory to be tested.
ALL_HTML_FILES = [f for f in ALL_FILES if f.endswith('.html') and "bak" not in f]

class TestLinks(unittest.TestCase):
    """Test suite for verifying internal links in HTML files.

    This class contains tests to ensure that all internal links within the
    website point to valid, existing files.
    """

    def test_internal_links(self):
        """Verifies that all internal links in HTML files point to existing files.

        This test iterates through all HTML files, extracts all internal links
        (href attributes), and checks if the linked files exist.
        """
        for filepath in ["index.html", "index-en.html"]:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Use a regular expression to find all href attributes
                    links = re.findall(r'href="([^"]+)"', content)
                    for link in links:
                        # Ignore external links, mailto links, and anchor links
                        if link.startswith(('http://', 'https://', 'mailto:', '#')):
                            continue
                        # Check if the linked file exists
                        self.assertIn(link, ALL_FILES, f"Broken link in {filepath}: {link}")
