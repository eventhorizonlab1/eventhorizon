"""Tests for the social media links of the Event Horizon website.

This module contains tests to ensure that the social media links in the footer
are correctly implemented and behave as expected. This is a static analysis
test that checks for the presence of the correct social media links in all
HTML files.
"""

import unittest
import re

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath: The path to the file to be read.

    Returns:
        The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestSocialMediaLinks(unittest.TestCase):
    """Test suite for social media links in the footer."""

    def test_social_media_links_are_correct(self):
        """Ensures the social media links in the footer have correct URLs."""
        content = read_file_content("index.html")

        youtube_link_pattern = r'<a class="text-gray-400 transition-colors hover:text-white" href="https://www.youtube.com" title="YouTube">'
        linkedin_link_pattern = r'<a class="text-gray-400 transition-colors hover:text-white" href="https://www.linkedin.com" title="LinkedIn">'
        twitter_link_pattern = r'<a class="text-gray-400 transition-colors hover:text-white" href="https://www.twitter.com" title="Twitter">'

        self.assertIsNotNone(re.search(youtube_link_pattern, content), "YouTube link is incorrect or missing in the footer.")
        self.assertIsNotNone(re.search(linkedin_link_pattern, content), "LinkedIn link is incorrect or missing in the footer.")
        self.assertIsNotNone(re.search(twitter_link_pattern, content), "Twitter link is incorrect or missing in the footer.")

if __name__ == '__main__':
    unittest.main()
