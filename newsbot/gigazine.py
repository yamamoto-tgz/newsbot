from datetime import datetime as dt

from newsbot.item import Item
from newsbot.rss import Rss


class Gigazine(Rss):
    def __init__(self):
        name = "gigazine"
        url = "https://gigazine.net/news/rss_2.0/"
        path = "./rss/gigazine.xml"
        super().__init__(name, url, path)

    def items(self):
        items = []

        try:
            for item in self.read()["rss"]["channel"]["item"]:
                title = item["title"]
                link = item["link"]
                datetime = dt.fromisoformat(item["dc:date"])
                subjects = item["dc:subject"][:-1].split(
                    ","
                )  # :-1 => Remove empty value
                source = self.name

                item = Item(title, link, datetime, subjects, source)

                items.append(item)

        finally:
            return items
