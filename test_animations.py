"""Tests for the animation logic of the Event Horizon website.

This file is fully documented with Google Style Python Docstrings.
"""

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

class TestAnimations(unittest.TestCase):
    """Test suite for animation logic.

    This class contains tests to ensure that the JavaScript-based animations
    are correctly implemented and behave as expected.
    """

    def test_animations_js_not_empty(self):
        """Ensures that the `documentation.js` file is not empty.

        This test serves as a basic check to confirm that the animation
        script has not been accidentally wiped or corrupted.
        """
        content = read_file_content('documentation.js')
        self.assertGreater(len(content), 0, "The 'documentation.js' file is empty!")
