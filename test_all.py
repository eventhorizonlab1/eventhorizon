
import asyncio
import http.server
import socket
import socketserver
import threading
import unittest
from playwright.async_api import async_playwright

def is_port_in_use(port):
    """Checks if a port is in use.

    Args:
        port: The port number to check.

    Returns:
        True if the port is in use, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

class TestWebsite(unittest.TestCase):
    """Test suite for the Event Horizon website."""

    @classmethod
    def setUpClass(cls):
        """Sets up the browser, event loop, and HTTP server for the test class.

        Raises:
            ConnectionError: If port 8000 is already in use.
        """
        if is_port_in_use(8000):
            raise ConnectionError("Port 8000 is already in use. Please close the process using it and try again.")

        socketserver.TCPServer.allow_reuse_address = True
        handler = http.server.SimpleHTTPRequestHandler
        cls.server = socketserver.TCPServer(("", 8000), handler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

        cls.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(cls.loop)
        cls.playwright = cls.loop.run_until_complete(async_playwright().start())
        cls.browser = cls.loop.run_until_complete(cls.playwright.chromium.launch(headless=True))

    @classmethod
    def tearDownClass(cls):
        """Tears down the browser, event loop, and HTTP server after the tests."""
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def setUp(self):
        """Sets up a new page for each test."""
        self.page = self.loop.run_until_complete(self.browser.new_page())
        self.loop.run_until_complete(self.page.emulate_media(reduced_motion='no-preference'))

    def tearDown(self):
        """Tears down the page after each test."""
        self.loop.run_until_complete(self.page.close())

    async def get_scroll_left(self, selector):
        """Gets the scrollLeft property of an element.

        Args:
            selector: The CSS selector of the element.

        Returns:
            The scrollLeft property of the element.
        """
        element = await self.page.query_selector(selector)
        return await element.evaluate('(node) => node.scrollLeft')

    async def get_theme_state(self):
        """Gets the current theme state.

        Returns:
            A tuple containing the theme state: (is_dark, icon_text, aria_pressed).
        """
        html = await self.page.query_selector('html')
        is_dark = 'dark' in (await html.get_attribute('class') or '')

        button = await self.page.query_selector('#theme-toggle')
        icon = await button.query_selector('span')
        icon_text = await icon.inner_text()

        aria_pressed = await button.get_attribute('aria-pressed')

        return is_dark, icon_text, aria_pressed

    def test_carousel_navigation_buttons(self):
        """Verifies that the carousel's next and previous buttons work correctly."""
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')
            await self.page.wait_for_selector('#articles .flex.snap-x')

            articles_carousel_selector = '#articles .flex.snap-x'
            next_button_selector = '#articles header button:nth-of-type(2)'
            prev_button_selector = '#articles header button:nth-of-type(1)'

            initial_scroll_left = await self.get_scroll_left(articles_carousel_selector)

            await self.page.hover('#articles')
            await self.page.click(next_button_selector)
            await self.page.wait_for_timeout(500)
            new_scroll_left = await self.get_scroll_left(articles_carousel_selector)
            self.assertGreater(new_scroll_left, initial_scroll_left)

            await self.page.click(prev_button_selector)
            await self.page.wait_for_timeout(500)
            final_scroll_left = await self.get_scroll_left(articles_carousel_selector)
            self.assertLess(final_scroll_left, new_scroll_left)

        self.loop.run_until_complete(run_test(self))

    def test_carousel_keyboard_navigation(self):
        """Verifies that the carousel's keyboard navigation works correctly."""
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')
            await self.page.wait_for_selector('#articles .flex.snap-x')

            articles_carousel_selector = '#articles .flex.snap-x'

            initial_scroll_left = await self.get_scroll_left(articles_carousel_selector)

            await self.page.focus(articles_carousel_selector)
            await self.page.keyboard.press('ArrowRight')
            await self.page.wait_for_timeout(500)
            scroll_left_after_right_arrow = await self.get_scroll_left(articles_carousel_selector)
            self.assertGreater(scroll_left_after_right_arrow, initial_scroll_left)

            await self.page.keyboard.press('ArrowLeft')
            await self.page.wait_for_timeout(500)
            scroll_left_after_left_arrow = await self.get_scroll_left(articles_carousel_selector)
            self.assertEqual(scroll_left_after_left_arrow, initial_scroll_left)

            await self.page.keyboard.press('End')
            await self.page.wait_for_timeout(500)
            scroll_left_after_end_key = await self.get_scroll_left(articles_carousel_selector)
            self.assertGreater(scroll_left_after_end_key, initial_scroll_left)

            await self.page.keyboard.press('Home')
            await self.page.wait_for_timeout(500)
            scroll_left_after_home_key = await self.get_scroll_left(articles_carousel_selector)
            self.assertEqual(scroll_left_after_home_key, initial_scroll_left)

        self.loop.run_until_complete(run_test(self))

    def test_theme_switcher(self):
        """Verifies that the theme switcher works correctly."""
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')

            await self.page.wait_for_selector('#theme-toggle')

            # Initial state should be light mode
            is_dark, icon_text, aria_pressed = await self.get_theme_state()
            self.assertFalse(is_dark)
            self.assertIn(icon_text, ['light_mode', 'dark_mode'])
            self.assertEqual(aria_pressed, 'false')

            # Click the theme toggle button to switch to dark mode
            await self.page.click('#theme-toggle')
            await self.page.wait_for_timeout(500)

            is_dark, icon_text, aria_pressed = await self.get_theme_state()
            self.assertTrue(is_dark)
            self.assertIn(icon_text, ['light_mode', 'dark_mode'])
            self.assertEqual(aria_pressed, 'true')

            # Click the theme toggle button again to switch back to light mode
            await self.page.click('#theme-toggle')
            await self.page.wait_for_timeout(500)

            is_dark, icon_text, aria_pressed = await self.get_theme_state()
            self.assertFalse(is_dark)
            self.assertIn(icon_text, ['light_mode', 'dark_mode'])
            self.assertEqual(aria_pressed, 'false')

        self.loop.run_until_complete(run_test(self))

if __name__ == '__main__':
    unittest.main()
