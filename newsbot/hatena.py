from datetime import datetime as dt
from datetime import timedelta, timezone

from newsbot.item import Item
from newsbot.rss import Rss


class Hatena(Rss):
    def __init__(self):
        url = "https://b.hatena.ne.jp/hotentry/it.rss"
        path = "./rss/hatena_it.xml"
        super().__init__(url, path)

    def items(self):
        items = []

        try:
            for item in self.read()["rdf:RDF"]["item"]:
                title = item["title"]
                link = item["link"]
                utc = dt.strptime(item["dc:date"], "%Y-%m-%dT%H:%M:%SZ").replace(
                    tzinfo=timezone.utc
                )
                datetime = utc.astimezone(timezone(timedelta(hours=9)))
                subjects = item["dc:subject"]
                source = "hatena"

                item = Item(title, link, datetime, subjects, source)

                items.append(item)

        finally:
            return items
