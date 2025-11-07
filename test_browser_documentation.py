import asyncio
import unittest
import os
from playwright.async_api import async_playwright

class TestBrowserDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        self.page = self.loop.run_until_complete(self.browser.new_page())

    def tearDown(self):
        self.loop.run_until_complete(self.page.close())

    def test_anime_is_defined(self):
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))
            anime_defined = await self.page.evaluate('typeof anime')
            self.assertEqual(anime_defined, 'function')

        self.loop.run_until_complete(run_test())

    def test_header_scroll_animation(self):
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))

            # Get header element
            header = await self.page.query_selector('header')
            self.assertIsNotNone(header, "Header element not found")

            # 1. Check initial state
            initial_class = await header.get_attribute('class')
            self.assertNotIn('scrolled', initial_class or '', "Header should not have 'scrolled' class initially")

            # 2. Scroll down and check for 'scrolled' class
            await self.page.evaluate('window.scrollTo(0, 100)')
            await self.page.wait_for_timeout(500)

            scrolled_class = await header.get_attribute('class')
            self.assertIn('scrolled', scrolled_class or '', "Header should have 'scrolled' class after scrolling down")

            # 3. Scroll back to top and check for 'scrolled' class removal
            await self.page.evaluate('window.scrollTo(0, 0)')
            await self.page.wait_for_timeout(500)

            final_class = await header.get_attribute('class')
            self.assertNotIn('scrolled', final_class or '', "Header should not have 'scrolled' class after scrolling to top")

        self.loop.run_until_complete(run_test())

    def test_quick_link_hover_effect(self):
        async def run_test():
            await self.page.goto('file://' + os.path.abspath('index.html'))

            # Find the "À Propos" link in the footer
            quick_link = await self.page.query_selector('footer a[href="a-propos.html"]')
            self.assertIsNotNone(quick_link, "Quick link not found")

            # 1. Check initial state
            initial_class = await quick_link.get_attribute('class')
            self.assertNotIn('text-primary', initial_class or '', "Quick link should not have 'text-primary' class initially")

            # 2. Hover over the link and check for 'text-primary' class
            await quick_link.hover()
            await self.page.wait_for_timeout(500) # Wait for animation

            hover_class = await quick_link.get_attribute('class')
            self.assertIn('text-primary', hover_class or '', "Quick link should have 'text-primary' class on hover")

            # 3. Move the mouse away and check for 'text-primary' class removal
            await self.page.mouse.move(0, 0)
            await self.page.wait_for_timeout(500) # Wait for animation

            final_class = await quick_link.get_attribute('class')
            self.assertNotIn('text-primary', final_class or '', "Quick link should not have 'text-primary' class after hover")

        self.loop.run_until_complete(run_test())

if __name__ == '__main__':
    unittest.main()
