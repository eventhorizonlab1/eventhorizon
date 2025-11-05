"""Tests to verify the integrity of internal links.

This file is fully documented with Google Style Python Docstrings.
"""

import os
import re
import unittest

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]
ALL_FILES = [f for f in os.listdir('.')]

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestLinks(unittest.TestCase):
    """Test suite for internal links.

    This class contains tests to ensure that all internal links on the website
    are valid and do not point to non-existent pages.
    """

    def test_internal_links(self):
        """Verifies that all internal links in HTML files point to existing files.

        This test iterates through all HTML files, extracts all internal links,
        and checks that the linked files exist in the project directory.
        """
        for filepath in HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                # Find all internal links (hrefs not starting with http)
                links = re.findall(r'href="([^"]+)"', content)
                internal_links = [l for l in links if not l.startswith('http') and not l.startswith('#')]

                for link in internal_links:
                    with self.subTest(link=link):
                        self.assertIn(link, ALL_FILES, f"Broken link in {filepath}: {link}")
