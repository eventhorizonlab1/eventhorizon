"""Tests for the animation logic of the Event Horizon website.

This module contains tests for the animation logic of the Event Horizon website.
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
    """Test suite for the animation logic in `documentation.js`.

    This class contains a static analysis test to ensure that the JavaScript
    file responsible for animations is present and not empty. This serves as a
    basic safeguard against accidental deletion or corruption of the animation
    script, which would break all visual interactivity on the website.
    """

    def test_animations_js_not_empty(self):
        """Ensures that the `documentation.js` file is not empty.

        This test serves as a basic check to confirm that the animation
        script has not been accidentally wiped or corrupted. An empty
        JavaScript file would break all animations and interactivity.
        """
        content = read_file_content('documentation.js')
        self.assertGreater(len(content), 0, "The 'documentation.js' file is empty!")
