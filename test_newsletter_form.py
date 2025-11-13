"""Tests for the newsletter form of the Event Horizon website.

This module contains tests to validate the structure of the newsletter form.
It ensures that the form and its input fields have the necessary attributes
for proper submission.
"""

import os
import re
import unittest
from bs4 import BeautifulSoup

HTML_FILES = [f for f in os.listdir('.') if f.endswith('.html')]


def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


class TestNewsletterForm(unittest.TestCase):
    """Test suite for the newsletter form.

    This class contains a static analysis test to ensure that the newsletter
    form is correctly structured. A properly structured form is essential for
    successful user subscriptions.
    """

    def test_newsletter_form_attributes(self):
        """Ensures the newsletter form is correctly structured.

        This test verifies that if a newsletter form is present on a page,
        it contains the necessary 'action' and 'method' attributes,
        and that the email input has a 'name' attribute. These attributes
        are essential for the form to be submitted correctly.
        """
        for filepath in HTML_FILES:
            with self.subTest(filepath=filepath):
                content = read_file_content(filepath)
                soup = BeautifulSoup(content, 'html.parser')

                # Find the div that contains the newsletter form
                newsletter_div = soup.find('div', class_='rounded-lg')

                if newsletter_div:
                    # Find the form within that div
                    newsletter_form = newsletter_div.find('form')

                    if newsletter_form:
                        self.assertTrue(newsletter_form.has_attr('action'), f"Missing 'action' attribute in newsletter form in {filepath}")
                        self.assertTrue(newsletter_form.has_attr('method'), f"Missing 'method' attribute in newsletter form in {filepath}")

                        email_input = newsletter_form.find('input', {'type': 'email'})
                        self.assertIsNotNone(email_input, f"Email input not found in newsletter form in {filepath}")
                        self.assertTrue(email_input.has_attr('name'), f"Missing 'name' attribute in email input in {filepath}")
