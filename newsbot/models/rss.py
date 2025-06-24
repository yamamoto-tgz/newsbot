import os
from dataclasses import dataclass
from datetime import datetime, timezone

import requests
import xmltodict

from newsbot.models.item import Item


@dataclass
class Rss:
    name: str
    url: str
    path: str
    version: str

    def download(self):
        dir = os.path.dirname(self.path)
        if not os.path.exists(dir):
            os.makedirs(dir)

        proxy = os.getenv("NB_PROXY")
        url = f"{proxy}?url={self.url}" if proxy else self.url

        response = requests.get(url)

        with open(self.path, "wb") as f:
            f.write(response.content)

    def items(self):
        with open(self.path, "r") as f:
            dict = xmltodict.parse(f.read())

        items = []

        if self.version == "2.0":
            for item in dict["rss"]["channel"]["item"]:
                items.append(Item(item["title"], item["link"], self._parse(item["pubDate"]), self.name))

        elif self.version == "1.0":
            for item in dict["rdf:RDF"]["item"]:
                items.append(Item(item["title"], item["link"], self._parse(item["dc:date"]), self.name))

        return items

    def _parse(self, datetime_str):
        if datetime_str.endswith("+0900"):
            return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %z")

        elif datetime_str.endswith("GMT"):
            return datetime.strptime(datetime_str, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)

        else:
            return datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
