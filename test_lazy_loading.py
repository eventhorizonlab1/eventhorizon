"""Tests for the lazy loading functionality of the Event Horizon website."""

import re
import unittest

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestLazyLoading(unittest.TestCase):
    """Test suite for lazy loading functionality."""

    def test_lazy_loading_on_index_page(self):
        """Verifies that images on the index page use lazy loading."""
        content = read_file_content('index.html')

        # Find all divs that should be lazy-loaded
        image_divs = re.findall(r'<div[^>]+data-alt="[^"]+"[^>]*>', content)

        # Check that each of these divs has the 'lazy' class and a 'data-src' attribute
        for div in image_divs:
            with self.subTest(div=div):
                self.assertIn('lazy', div, f"Image div does not have the 'lazy' class: {div}")
                self.assertIn('data-src', div, f"Image div does not have the 'data-src' attribute: {div}")
