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

        # Isolate the mouseleave event listener
        mouseleave_match = re.search(
            r'link\.addEventListener\("mouseleave", \(\) => \{.*?\}\);',
            function_code,
            re.DOTALL
        )
        self.assertIsNotNone(mouseleave_match, "The mouseleave event listener was not found.")

        mouseleave_code = mouseleave_match.group(0)

        # Check that if color is used, it's dependent on the theme
        color_line_match = re.search(r'.*color:.*', mouseleave_code)
        if color_line_match:
            color_line = color_line_match.group(0)
            self.assertIn(
                'isDark',
                color_line,
                "The color property should be dependent on the theme (isDark variable)."
            )

if __name__ == '__main__':
    unittest.main()
