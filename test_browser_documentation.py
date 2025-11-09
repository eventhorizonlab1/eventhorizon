"""Verifies that the website's JavaScript functions are working correctly.

This module contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that the JavaScript functions in
`documentation.js` are behaving as expected.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserDocumentation(unittest.TestCase):
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

    def test_anime_is_defined(self):
        """Verifies that the anime.js library is defined on the page.

        This test ensures that the `anime` function is available in the global
        scope, which is crucial for all animations to work.
        """
        async def run_test():
            """Runs the anime.js definition test steps."""
            await self.page.goto('file://' + os.path.abspath('index.html'))
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
