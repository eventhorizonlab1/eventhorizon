import unittest
import re

def read_file_content(filepath):
    """Reads and returns the content of a given file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestLinkCheckerLogic(unittest.TestCase):
    def test_no_redundant_link_check_logic(self):
        """
        Verifies that there is no redundant 'if' statement for 'a-propos.html'
        in test_links.py, ensuring the test logic is clean and maintainable.
        """
        content = read_file_content('test_links.py')
        pattern = r'if link == "a-propos.html":'
        self.assertNotRegex(
            content,
            pattern,
            "Found redundant 'if' statement for 'a-propos.html' in test_links.py."
        )
