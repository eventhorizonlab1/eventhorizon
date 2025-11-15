"""Consolidated browser-based tests for the Event Horizon website.

This module contains a comprehensive suite of browser-based tests,
using Playwright to ensure that animations, interactive elements, and
internationalization are functioning correctly.
"""

import asyncio
import http.server
import socket
import socketserver
import threading
import unittest
from playwright.async_api import async_playwright

def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

class TestBrowser(unittest.TestCase):
    """Test suite for browser-based functionality.

    This class sets up a Playwright browser instance and a local HTTP server
    to run tests that verify the correct behavior of animations, interactive
    elements, and language switching on the website.
    """

    @classmethod
    def setUpClass(cls):
        """Sets up the browser, event loop, and HTTP server for the test class."""
        if is_port_in_use(8000):
            raise ConnectionError("Port 8000 is already in use. Please close the process using it and try again.")

        # Allow the server to reuse the address to avoid "Address already in use" errors
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

    def tearDown(self):
        """Tears down the page after each test."""
        self.loop.run_until_complete(self.page.close())

    def test_page_title(self):
        """Verifies that the page title is correct."""
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')
            self.assertEqual(await self.page.title(), "Event Horizon - Dans les coulisses de l'industrie spatiale européenne")
        self.loop.run_until_complete(run_test(self))

    def test_navigation_scroll(self):
        """Verifies that clicking the navigation links scrolls to the correct section."""
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')
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
        self.loop.run_until_complete(run_test(self))

    def test_translation_error_handling(self):
        """Verifies that a failed translation file request is handled gracefully."""
        async def run_test(self):
            error_message = ""
            def handle_console_message(msg):
                nonlocal error_message
                if msg.type == 'error':
                    error_message = msg.text

            self.page.on('console', handle_console_message)

            await self.page.route("**/locales/*.json", lambda route: route.abort())
            await self.page.goto('http://localhost:8000/index.html')

            await self.page.wait_for_timeout(1000)

            self.assertIn("Failed to load translations", error_message)
        self.loop.run_until_complete(run_test(self))

    def test_carousel_scroll(self):
        async def run_test(self):
            await self.page.goto('http://localhost:8000/index.html')

            # Test the articles carousel
            articles_carousel = await self.page.query_selector('#articles .snap-x')
            await articles_carousel.evaluate('(node) => node.scrollTo(500, 0)')
            await self.page.wait_for_timeout(500)
            scroll_left = await articles_carousel.evaluate('(node) => node.scrollLeft')
            self.assertGreater(scroll_left, 0)

            # Test the ecosystem carousel
            ecosystem_carousel = await self.page.query_selector('#ecosysteme .snap-x')
            await ecosystem_carousel.evaluate('(node) => node.scrollTo(500, 0)')
            await self.page.wait_for_timeout(500)
            scroll_left = await ecosystem_carousel.evaluate('(node) => node.scrollLeft')
            self.assertGreater(scroll_left, 0)

        self.loop.run_until_complete(run_test(self))
