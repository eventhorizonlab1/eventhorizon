"""Tests for the presence of calls to undefined functions in JavaScript files.

This file is fully documented with Google Style Python Docstrings.
"""

import unittest
import re

class TestUndefinedFunctions(unittest.TestCase):
    """Test suite for undefined function calls.

    This class contains tests to ensure that there are no calls to undefined
    functions in the JavaScript code.
    """

    def test_no_undefined_function_calls(self):
        """Asserts that there are no calls to 'setupThemeToggleGlow'.

        This test performs a static analysis of `documentation.js` to prevent
        the reintroduction of a latent bug—a commented-out call to an
        undefined function. If this test fails, it means the line has been
        uncommented, which could break the site's JavaScript functionality.
        """
        with open('documentation.js', 'r') as f:
            content = f.read()

        # This regex looks for the exact function call, ignoring whether it is commented out or not.
        # The bug report states that the line should be removed entirely, so this check is sufficient.
        match = re.search(r'setupThemeToggleGlow\(\)', content)
        self.assertIsNone(match, "A call to the undefined function 'setupThemeToggleGlow' was found in documentation.js")

if __name__ == '__main__':
    unittest.main()
