"""Verifies that browser animations and interactions work as expected.

This script contains a suite of browser-based tests for the Event Horizon
website, using Playwright to ensure that animations and interactive elements
are functioning correctly.
This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserAnimations(unittest.TestCase):
    """Test suite for browser-based animations and interactions.

    This class sets up a Playwright browser instance and runs tests to verify
    the correct behavior of animations and interactive elements on the website.
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

    def test_page_title(self):
        """Verifies that the page title is correct."""
        async def run_test():
            await self.page.goto('file://'
                                 + os.path.abspath('index.html'))
            self.assertEqual(await self.page.title(), "Event Horizon - Dans les coulisses de l'industrie spatiale européenne")
        self.loop.run_until_complete(run_test())

    def test_navigation_scroll(self):
        """Verifies that clicking the navigation links scrolls to the correct section."""
        async def run_test():
            await self.page.goto('file://'
                                 + os.path.abspath('index.html'))
            await self.page.click('a[href="#videos"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            videos_section = await self.page.query_selector('#videos')
            self.assertTrue(await videos_section.is_visible())

            await self.page.click('a[href="#articles"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            articles_section = await self.page.query_selector('#articles')
            self.assertTrue(await articles_section.is_visible())

            await self.page.click('a[href="#ecosysteme"]')
            await self.page.wait_for_timeout(1000)  # Wait for scroll animation
            ecosysteme_section = await self.page.query_selector('#ecosysteme')
            self.assertTrue(await ecosysteme_section.is_visible())
        self.loop.run_until_complete(run_test())
