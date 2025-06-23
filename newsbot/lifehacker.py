from datetime import datetime as dt
from datetime import timedelta, timezone

from newsbot.item import Item
from newsbot.rss import Rss


class Lifehacker(Rss):
    def __init__(self):
        name = "lifehacker"
        url = "https://www.lifehacker.jp/feed/"
        path = "./rss/lifehacker.xml"
        super().__init__(name, url, path)

    def items(self):
        items = []

        try:
            for item in self.read()["rss"]["channel"]["item"]:
                title = item["title"]
                link = item["link"]
                utc = dt.strptime(item["pubDate"], "%a, %d %b %Y %H:%M:%S %Z").replace(
                    tzinfo=timezone.utc
                )
                datetime = utc.astimezone(timezone(timedelta(hours=9)))
                subjects = []
                source = self.name

                item = Item(title, link, datetime, subjects, source)

                items.append(item)

        finally:
            return items
