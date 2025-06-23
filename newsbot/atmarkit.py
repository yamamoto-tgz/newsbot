from datetime import datetime as dt

from newsbot.item import Item
from newsbot.rss import Rss


class Atmarkit(Rss):
    def __init__(self):
        name = "atmarkit"
        url = "https://rss.itmedia.co.jp/rss/2.0/ait.xml"
        path = "./rss/atmarkit.xml"
        super().__init__(name, url, path)

    def items(self):
        items = []

        try:
            for item in self.read()["rss"]["channel"]["item"]:
                title = item["title"]
                link = item["link"]
                datetime = dt.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %z")
                subjects = []
                source = self.name

                item = Item(title, link, datetime, subjects, source)

                items.append(item)

        finally:
            return items
