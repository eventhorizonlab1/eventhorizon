"""
This test module verifies that the quick link hover animation
does not use a hardcoded color, which would cause issues when
the theme is changed.
"""

import re
import unittest

def read_file_content(filepath):
    """Reads and returns the content of a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestHardcodedHoverColor(unittest.TestCase):
    """
    Test suite for the quick link hover animation to ensure it is
    theme-change friendly.
    """

    def test_no_hardcoded_color_on_mouseenter(self):
        """
        Verifies that the '.quick-link' mouseenter event listener
        does not contain a hardcoded color.
        """
        content = read_file_content('documentation.js')

        # Find the mouseenter event listener for quickLinks
        mouseenter_match = re.search(
            r"link\.addEventListener\('mouseenter', \(\) => {([^}]+)}\);",
            content,
            re.DOTALL
        )
        self.assertIsNotNone(
            mouseenter_match,
            "Could not find the mouseenter event listener for '.quick-link'."
        )

        # Check that the color is not hardcoded in the mouseenter animation
        animation_block = mouseenter_match.group(1)
        self.assertNotIn(
            "link.style.color",
            animation_block,
            "A hardcoded color is set in the mouseenter animation for '.quick-link'."
        )
