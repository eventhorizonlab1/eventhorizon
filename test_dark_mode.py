"""Tests for the dark mode functionality of the Event Horizon website.

This file is fully documented with Google Style Python Docstrings.
"""

import re
import unittest
import asyncio
from playwright.async_api import async_playwright
import os

def read_file_content(filepath):
    """Reads and returns the content of a given file.

    Args:
        filepath (str): The path to the file to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

class TestDarkMode(unittest.TestCase):
    """Test suite for dark mode functionality.

    This class contains tests to ensure that the dark mode feature is
    implemented correctly and that theme-dependent animations are theme-aware.
    """

    def test_quick_link_dark_mode_color_reset(self):
        """Verifies that '.quick-link' hover animation is theme-aware.

        This test checks the mouseleave event listener in `documentation.js`
        to ensure that the text color is not hardcoded, which would cause
        issues in dark mode.
        """
        content = read_file_content('documentation.js')

        # Find the mouseleave event listener for quickLinks within setupQuickLinkHovers
        mouseleave_match = re.search(r"link\.addEventListener\('mouseleave', \(\) => {([^}]+)}\);", content, re.DOTALL)
        self.assertIsNotNone(mouseleave_match, "Could not find the mouseleave event listener for '.quick-link'.")

        animation_block = mouseleave_match.group(1)

        # Check that the color is not hardcoded to the light theme value.
        hardcoded_color = "color: 'rgba(0, 0, 0, 0.6)'"
        self.assertNotIn(hardcoded_color, animation_block,
            f"Found hardcoded light-theme color '{hardcoded_color}' in the mouseleave animation for '.quick-link'. "
            "This is incorrect for dark mode."
        )

class TestBrowserDarkMode(unittest.TestCase):
    """Test suite for browser-based dark mode functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up the browser and page objects for the test class."""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch())

    @classmethod
    def tearDownClass(cls):
        """Tear down the browser and page objects for the test class."""
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Set up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Close the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_theme_toggle(self):
        """Verifies that the theme toggle button works correctly.

        This test loads the index.html page, clicks the theme toggle button,
        and verifies that the `dark` class is applied to the `<html>` element
        and that the theme toggle icon is updated.
        """
        async def run_test(page):
            # Get the absolute path to the HTML file
            file_path = os.path.abspath('index.html')
            await page.goto(f'file://{file_path}')

            # Get the theme toggle button and icon
            theme_toggle_button = await page.query_selector('#theme-toggle')
            self.assertIsNotNone(theme_toggle_button, "The theme toggle button was not found.")
            theme_toggle_icon = await theme_toggle_button.query_selector('span')
            self.assertIsNotNone(theme_toggle_icon, "The theme toggle icon was not found.")

            # Check the initial state (light mode)
            html_element = await page.query_selector('html')
            self.assertFalse('dark' in await html_element.get_attribute('class'),
                "The `dark` class was present on the `<html>` element on initial load.")
            self.assertEqual(await theme_toggle_icon.text_content(), 'light_mode',
                "The theme toggle icon was not in the correct initial state.")

            # Click the theme toggle button
            await theme_toggle_button.click()

            # Wait for the animation to complete
            await page.wait_for_timeout(1000)

            # Check the final state (dark mode)
            self.assertTrue('dark' in await html_element.get_attribute('class'),
                "The `dark` class was not applied to the `<html>` element after toggling the theme.")
            self.assertEqual(await theme_toggle_icon.text_content(), 'dark_mode',
                "The theme toggle icon was not updated after toggling the theme.")

        # Run the async test
        self.loop.run_until_complete(run_test(self.page))
