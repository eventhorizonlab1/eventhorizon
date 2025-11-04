"""Tests for the dark mode functionality of the Event Horizon website.

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

class TestDarkMode(unittest.TestCase):
    """Test suite for dark mode functionality.

    This class contains tests to ensure that the dark mode feature is
    implemented correctly and that theme-dependent animations are theme-aware.
    """

    def test_quick_link_dark_mode_color_reset(self):
        """Verifies that '.quick-link' hover animation is theme-aware.

        This test checks the mouseleave event listener in `documentation.js`
        to ensure that the text color is not hardcoded, which would cause
        issues in dark mode.
        """
        content = read_file_content('documentation.js')

        # Find the mouseleave event listener for quickLinks within setupQuickLinkHovers
        mouseleave_match = re.search(r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);", content, re.DOTALL)
        self.assertIsNotNone(mouseleave_match, "Could not find the mouseleave event listener for '.quick-link'.")

        animation_block = mouseleave_match.group(1)

        # Check that the color is not hardcoded to the light theme value.
        hardcoded_color = "color: 'rgba(0, 0, 0, 0.6)'"
        self.assertNotIn(hardcoded_color, animation_block,
            f"Found hardcoded light-theme color '{hardcoded_color}' in the mouseleave animation for '.quick-link'. "
            "This is incorrect for dark mode."
        )
