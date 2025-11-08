
import os
import unittest

ALL_HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html') and "bak" not in f]

class TestFooterLinks(unittest.TestCase):
    def test_footer_links(self):
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    if "-en" in filepath:
                        self.assertNotIn('>About</a>', content)
                    else:
                        self.assertNotIn('>À Propos</a>', content)
                    self.assertIn('href="mailto:contact@eventhorizon.fr"', content)
