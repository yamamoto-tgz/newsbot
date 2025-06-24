import sqlite3
from dataclasses import dataclass
from datetime import datetime, timezone

import dateutil.parser as dateparser

DATABASE = "newsbot.db"


@dataclass
class Article:
    channel: str
    title: str
    link: str
    published: str
    created: str

    def time(self):
        diff = datetime.now(timezone.utc) - dateparser.parse(self.published)
        seconds = diff.total_seconds()

        if seconds < 60:
            return "now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h"
        else:
            days = int(seconds // 86400)
            return f"{days}d"

    @staticmethod
    def create_table():
        with sqlite3.connect(DATABASE) as con:
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS articles (channel, title, link, published, created, PRIMARY KEY (channel, title, link))"
            )

    @staticmethod
    def bulk_insert(articles):
        with sqlite3.connect(DATABASE) as con:
            sql = f"INSERT INTO articles (channel, title, link, published, created) VALUES (?, ?, ?, ?, ?) ON CONFLICT DO NOTHING"
            rowcount = con.cursor().executemany(sql, articles).rowcount
            return rowcount

    @staticmethod
    def delete_older_than(iso_date):
        with sqlite3.connect(DATABASE) as con:
            sql = f"DELETE FROM articles WHERE created < ?"
            rowcount = con.cursor().execute(sql, [iso_date]).rowcount
            return rowcount

    @staticmethod
    def find_all_order_by_published_desc():
        with sqlite3.connect(DATABASE) as con:
            sql = "SELECT * FROM articles ORDER BY published DESC"
            rows = con.cursor().execute(sql).fetchall()
            return [Article(*row) for row in rows]
