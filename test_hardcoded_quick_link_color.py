"""Tests for the quick link hover animation.

This module verifies that the hover animation for the quick links in the footer
does not use a hardcoded color. Hardcoding colors in JavaScript can lead to
inconsistencies when the website's theme is updated.
"""

import re
import unittest

class TestQuickLinkHoverAnimation(unittest.TestCase):
    """Test suite for the quick link hover animation.

    This class contains tests to ensure that the quick link hover animation
    does not use a hardcoded color.
    """

    def test_hover_animation_does_not_use_hardcoded_color(self):
        """Verifies that the quick link hover animation does not use a hardcoded color.

        This test reads the content of the `documentation.js` file and uses a
        regular expression to check that the `setupQuickLinkHovers` function
        does not contain a hardcoded color property. This ensures that the
        animation is theme-agnostic and will not cause issues when the theme
        is changed. A theme-aware application should not have hardcoded colors.
        """
        with open('documentation.js', 'r', encoding='utf-8') as f:
            js_code = f.read()

        # Isolate the setupQuickLinkHovers function
        match = re.search(
            r'function setupQuickLinkHovers\(\) \{.*?\}(?=\n\n|\Z)',
            js_code,
            re.DOTALL
        )
        self.assertIsNotNone(match, "The setupQuickLinkHovers function was not found.")

        function_code = match.group(0)

        # Check for hardcoded color in the mouseleave event listener
        self.assertNotIn(
            'color:',
            function_code,
            "The quick link hover animation should not use a hardcoded color."
        )

if __name__ == '__main__':
    unittest.main()
