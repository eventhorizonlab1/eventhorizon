"""Tests for the theme icon toggle on the Event Horizon website.

This module uses Playwright to simulate user interactions and verify
that the theme icon toggles correctly between light and dark modes.
This file is fully documented with Google Style Python Docstrings.
"""

import asyncio
import unittest
from playwright.async_api import async_playwright

class TestThemeIcon(unittest.TestCase):
    """Test suite for the theme icon toggle.

    This class contains tests that use Playwright to interact with the website
    and verify that the theme icon toggles correctly.
    """
    async def async_setup(self):
        """Initializes the Playwright browser instance."""
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()

    async def async_teardown(self):
        """Closes the Playwright browser instance."""
        await self.browser.close()
        await self.playwright.stop()

    def test_theme_icon_toggle(self):
        """Verifies that the theme icon toggles correctly."""
        async def test_logic():
            """The core logic for the test."""
            await self.async_setup()
            try:
                await self.page.goto("file:///app/index.html")

                # Check initial state (light mode)
                light_icon = self.page.locator(".light-icon")
                dark_icon = self.page.locator(".dark-icon")

                self.assertTrue(await light_icon.is_visible(), "Light icon should be visible in light mode")
                self.assertFalse(await dark_icon.is_visible(), "Dark icon should be hidden in light mode")

                # Toggle to dark mode
                await self.page.click("#theme-toggle")
                await self.page.wait_for_timeout(500)  # Wait for animation

                # Check dark mode
                self.assertFalse(await light_icon.is_visible(), "Light icon should be hidden in dark mode")
                self.assertTrue(await dark_icon.is_visible(), "Dark icon should be visible in dark mode")

            finally:
                await self.async_teardown()

        asyncio.run(test_logic())

if __name__ == "__main__":
    unittest.main()
