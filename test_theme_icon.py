
import asyncio
import unittest
from playwright.async_api import async_playwright

class TestThemeIcon(unittest.TestCase):
    async def async_setup(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch()
        self.page = await self.browser.new_page()

    async def async_teardown(self):
        await self.browser.close()
        await self.playwright.stop()

    def test_theme_icon_toggle(self):
        async def test_logic():
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
