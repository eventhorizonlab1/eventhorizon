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

class TestQuickLinkThemeChange(unittest.TestCase):
    """
    Test suite for the quick link hover animation to ensure it is
    theme-change friendly.
    """

    def test_no_hardcoded_color_on_mouseleave(self):
        """
        Verifies that the '.quick-link' mouseleave event listener
        does not contain a hardcoded color.
        """
        content = read_file_content('documentation.js')

        # Find the mouseleave event listener for quickLinks
        mouseleave_match = re.search(
            r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);",
            content,
            re.DOTALL
        )
        self.assertIsNotNone(
            mouseleave_match,
            "Could not find the mouseleave event listener for '.quick-link'."
        )

        # Check that the color is not hardcoded in the mouseleave animation
        animation_block = mouseleave_match.group(1)
        self.assertNotIn(
            "color:",
            animation_block,
            "A hardcoded color is set in the mouseleave animation for '.quick-link'."
        )
