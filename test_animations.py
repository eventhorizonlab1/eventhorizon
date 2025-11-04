"""Tests for the animation logic of the Event Horizon website."""

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
    """Test suite for animation logic."""

    def test_quick_link_hover_animation(self):
        """Verifies that the '.quick-link' hover animation resets text color.

        This test checks the mouseleave event listener in `documentation.js`
        to ensure that it contains an animation that resets the `color`
        property, preventing links from staying colored after the hover ends.
        """
        content = read_file_content('documentation.js')

        # Find the mouseleave event listener for quickLinks
        mouseleave_match = re.search(r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);", content, re.DOTALL)
        self.assertIsNotNone(mouseleave_match, "Could not find the mouseleave event listener for '.quick-link'.")

        # Check that the color is reset in the mouseleave animation
        animation_block = mouseleave_match.group(1)
        self.assertIn("color:", animation_block, "The color is not reset in the mouseleave animation for '.quick-link'.")
