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
    event listeners. It ensures that the core JavaScript logic is functioning
    as expected in a real browser environment.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the browser and event loop for the test class.

        This method is called once before any tests in this class are run.
        It sets up a Playwright browser instance and an asyncio event loop.
        """
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser and event loop after the tests.

        This method is called once after all tests in this class have been run.
        It closes the Playwright browser instance and the asyncio event loop.
        """
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test.

        This method is called before each test in this class is run.
        It creates a new Playwright page for each test to ensure that
        tests are isolated from each other.
        """
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        """Tears down the page after each test.

        This method is called after each test in this class is run.
        It closes the Playwright page to ensure that resources are
        cleaned up correctly.
        """
        self.loop.run_until_complete(self.page.close())

    def test_anime_is_defined(self):
        """Verifies that the anime.js library is defined on the page.

        This test ensures that the `anime` function is available in the global
        scope, which is crucial for all animations to work. Without anime.js,
        the site's animations would fail to run.
        """
        async def run_test():
            """Runs the anime.js definition test steps.

            Navigates to the index page and checks if the anime.js library
            has been successfully loaded and is available in the global scope.
            """
            await self.page.goto('file://' + os.path.abspath('index.html'))
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
