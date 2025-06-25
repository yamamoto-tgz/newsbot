import unittest

import requests


class TestNewsBot(unittest.TestCase):

    def test_nhk(self):
        self._test("nhk", "https://www.nhk.or.jp/rss/news/cat0.xml")

    def test_atmarkit(self):
        self._test("atmarkit", "https://rss.itmedia.co.jp/rss/2.0/ait.xml")

    def test_codezine(self):
        self._test("codezine", "https://codezine.jp/rss/new/20/index.xml")

    def test_gizmodo(self):
        self._test("gizmodo", "https://www.gizmodo.jp/index.xml")

    def test_itmedia(self):
        self._test("itmedia", "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml")

    def test_zenn(self):
        self._test("zenn", "https://zenn.dev/feed")

    def test_lifehacker(self):
        self._test("lifehacker", "https://www.lifehacker.jp/feed/")

    def test_gigazine(self):
        self._test("gigazine", "https://gigazine.net/news/rss_2.0/")

    def test_hatena(self):
        self._test("hatena", "https://b.hatena.ne.jp/hotentry/it.rss")

    def test_dznet(self):
        self._test("dznet", "http://feed.japan.zdnet.com/rss/index.rdf")

    def test_forest(self):
        self._test("forest", "https://forest.watch.impress.co.jp/data/rss/1.0/wf/feed.rdf")

    def test_gbusiness(self):
        self._test("gbusiness", "https://www.gamebusiness.jp/rss20/index.rdf")

    def test_gihyo(self):
        self._test("gihyo", "https://gihyo.jp/feed/rss2")

    def _test(self, channel, url):
        # Get
        xml = requests.get(url).content

        # Post
        headers = {"Content-Type": "application/xml"}
        response = requests.post(f"http://localhost:5000/xml/{channel}", data=xml, headers=headers)

        self.assertEqual(201, response.status_code)
        self.assertEqual("OK", response.text)
