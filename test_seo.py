import unittest
from test import read_file_content, ALL_HTML_FILES

class TestSEO(unittest.TestCase):
    def test_meta_descriptions_present(self):
        """Vérifie que toutes les pages ont une meta description."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                self.assertIn('<meta name="description"', content)
