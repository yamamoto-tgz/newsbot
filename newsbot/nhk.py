from datetime import datetime as dt

from newsbot.item import Item
from newsbot.rss import Rss


class Nhk(Rss):
    def __init__(self):
        name = "nhk"
        url = "https://www.nhk.or.jp/rss/news/cat0.xml"
        path = "./rss/nhk.xml"
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
