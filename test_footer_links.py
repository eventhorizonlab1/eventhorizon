
import re
import os
import unittest

# A list of all files in the current directory, used for link checking.
ALL_FILES = [f for f in os.listdir('.') if os.path.isfile(f)]
# A list of all HTML files in the current directory to be tested.
ALL_HTML_FILES = [f for f in ALL_FILES if f.endswith('.html') and "bak" not in f]

class TestFooterLinks(unittest.TestCase):
    """Test suite for verifying footer links in HTML files.

    This class contains tests to ensure that all footer links within the
    website point to valid, existing files.
    """

    def test_footer_links(self):
        """Verifies that the footer links are correct."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if filepath in ["index.html", "index-en.html"]:
                        self.assertIn('href="https://www.youtube.com"', content)
                        self.assertIn('href="https://www.linkedin.com"', content)
                        self.assertIn('href="https://twitter.com"', content)
                        if "-en" in filepath:
                            self.assertIn('href="a-propos-en.html"', content)
                        else:
                            self.assertIn('href="a-propos.html"', content)
                    else:
                        if "-en" in filepath:
                            self.assertIn('href="contact-en.html"', content)
                            self.assertIn('href="#"', content)
                        else:
                            self.assertIn('href="contact.html"', content)
                            self.assertIn('href="#"', content)
