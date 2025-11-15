
import unittest
import asyncio
import http.server
import socketserver
import threading
from playwright.async_api import async_playwright

class TestAnimations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

        cls.loop.run_until_complete(cls.browser.close())
        cls.loop.run_until_complete(cls.playwright.stop())
        cls.loop.close()

    def test_anime_is_defined_on_all_pages(self):
        """Checks that the anime.js library is defined on all relevant pages."""
        pages_to_test = ["index.html", "black_hole.html"]
        for page_path in pages_to_test:
            with self.subTest(page=page_path):
                self.loop.run_until_complete(self.check_anime_defined(page_path))

    async def check_anime_defined(self, page_path):
        page = await self.browser.new_page()
        await page.goto(f"http://localhost:8000/{page_path}")

        # Check if anime is defined in the global scope
        anime_is_defined = await page.evaluate("typeof anime !== 'undefined'")

        self.assertTrue(anime_is_defined, f"anime.js is not defined on {page_path}")

        await page.close()

if __name__ == '__main__':
    unittest.main()
