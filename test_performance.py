import unittest
from bs4 import BeautifulSoup
from test import read_file_content, ALL_HTML_FILES

class TestPerformance(unittest.TestCase):
    def test_images_have_alt_text(self):
        """Vérifie que toutes les images ont un texte alt."""
        for filepath in ALL_HTML_FILES:
            with self.subTest(filepath=filepath):
                soup = BeautifulSoup(read_file_content(filepath), 'html.parser')
                images = soup.find_all('img')
                for img in images:
                    self.assertTrue(img.has_attr('alt'))
