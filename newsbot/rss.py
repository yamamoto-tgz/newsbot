import os
from abc import ABC, abstractmethod

import requests
import xmltodict

from newsbot.item import Item


class Rss(ABC):
    def __init__(self, name, url, path):
        self.name = name
        self.url = url
        self.path = path

    def download(self):
        try:
            dir = os.path.dirname(self.path)
            if not os.path.exists(dir):
                os.makedirs(dir)

            proxy = os.getenv("NB_PROXY")
            url = f"{proxy}?url={self.url}" if proxy else self.url

            response = requests.get(url)
            print(f"download from {self.url} to {self.path}")

            with open(self.path, "wb") as f:
                f.write(response.content)

        except Exception as e:
            print(e)
            os.remove(self.path)

    def read(self):
        with open(self.path, "r") as f:
            xml = f.read()
            return xmltodict.parse(xml)

    @abstractmethod
    def items(self) -> list[Item]:
        pass
