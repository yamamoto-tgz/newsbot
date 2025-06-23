from datetime import datetime as dt

from newsbot.item import Item
from newsbot.rss import Rss


class Itmedia(Rss):
    def __init__(self):
        name = "itmedia"
        url = "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml"
        path = "./rss/itmedia.xml"
        super().__init__(name, url, path)

    def items(self):
        items = []

        try:
            for item in self.read()["rss"]["channel"]["item"]:
                title = item["title"]
                link = item["link"]
                datetime = dt.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
                source = self.name

                item = Item(title, link, datetime, source)

                items.append(item)

        finally:
            return items
