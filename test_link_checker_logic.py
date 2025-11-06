"""Tests for the link checker logic in the Event Horizon website.

This module verifies that there is no redundant link check logic in
`test_links.py`, ensuring that the test logic is clean and maintainable.
This file is fully documented with Google Style Python Docstrings.
"""

import unittest
import re

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestLinkCheckerLogic(unittest.TestCase):
    """Test suite for the link checker logic.

    This class contains tests to ensure that the link checker logic is
    not redundant.
    """
    def test_no_redundant_link_check_logic(self):
        """Verifies that there is no redundant 'if' statement for 'a-propos.html'
        in test_links.py, ensuring the test logic is clean and maintainable.
        """
        content = read_file_content('test_links.py')
        pattern = r'if link == "a-propos.html":'
        self.assertNotRegex(
            content,
            pattern,
            "Found redundant 'if' statement for 'a-propos.html' in test_links.py."
        )
