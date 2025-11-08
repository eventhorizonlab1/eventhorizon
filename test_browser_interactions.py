"""Verifies that the website's JavaScript functions are working correctly.

This script contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that the JavaScript functions in
`documentation.js` are behaving as expected.
This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserInteractions(unittest.TestCase):
    """Test suite for JavaScript functionality in the browser.

    This class sets up a Playwright browser instance and runs tests to verify
    the correct behavior of JavaScript functions, such as animations and
    event listeners.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the browser and event loop for the test class."""
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser and event loop after the tests."""
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Tears down the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_theme_switcher_toggle(self):
        """Verifies that the theme switcher toggles the 'dark' class.

        This test simulates a user clicking the theme switcher button and
        checks that the 'dark' class is added to and removed from the <html>
        element, and that localStorage is updated accordingly.
        """
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))

            # Get the html element and the theme switcher button
            html = await self.page.query_selector('html')
            theme_switcher = await self.page.query_selector('#theme-switcher')

            self.assertIsNotNone(html, "<html> element not found")
            self.assertIsNotNone(theme_switcher, "Theme switcher not found")

            # 1. Check initial state (should be light theme by default)
            initial_class = await html.get_attribute('class')
            self.assertNotIn('dark', initial_class or '', "<html> element should not have 'dark' class initially")
            initial_storage = await self.page.evaluate('localStorage.getItem("theme")')
            self.assertIn(initial_storage, [None, 'light'], "localStorage theme should be null or 'light' initially")


            # 2. Click to toggle to dark mode
            await theme_switcher.click()
            await self.page.wait_for_timeout(500) # Wait for JS to execute

            dark_class = await html.get_attribute('class')
            self.assertIn('dark', dark_class or '', "<html> element should have 'dark' class after first click")
            dark_storage = await self.page.evaluate('localStorage.getItem("theme")')
            self.assertEqual(dark_storage, 'dark', "localStorage theme should be 'dark'")


            # 3. Click again to toggle back to light mode
            await theme_switcher.click()
            await self.page.wait_for_timeout(500) # Wait for JS to execute

            light_class = await html.get_attribute('class')
            self.assertNotIn('dark', light_class or '', "<html> element should not have 'dark' class after second click")
            light_storage = await self.page.evaluate('localStorage.getItem("theme")')
            self.assertEqual(light_storage, 'light', "localStorage theme should be 'light'")


        self.loop.run_until_complete(run_test())


if __name__ == '__main__':
    unittest.main()
