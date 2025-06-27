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
    published: datetime
    created: datetime

    def time(self):
        diff = datetime.now(timezone.utc) - self.published.replace(tzinfo=timezone.utc)
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

    def is_newer_than(self, threshold):
        return self.published > threshold

    @staticmethod
    def from_row(row):
        return Article(*row)

    @staticmethod
    def create_table():
        with sqlite3.connect(DATABASE) as con:
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS articles (channel TEXT, title TEXT, link TEXT, published TIMESTAMP, created TIMESTAMP, PRIMARY KEY (channel, title, link))"
            )

    @staticmethod
    def bulk_insert(articles):
        with sqlite3.connect(DATABASE) as con:
            sql = f"INSERT INTO articles (channel, title, link, published, created) VALUES (?, ?, ?, datetime(?), datetime(?)) ON CONFLICT DO NOTHING"
            values = [list(article.__dict__.values()) for article in articles]
            rowcount = con.cursor().executemany(sql, values).rowcount
            return rowcount

    @staticmethod
    def delete_older_than(dt: datetime):
        with sqlite3.connect(DATABASE) as con:
            sql = f"DELETE FROM articles WHERE created < datetime(?)"
            rowcount = con.cursor().execute(sql, [dt]).rowcount
            return rowcount

    @staticmethod
    def find_all_order_by_published_desc():
        with sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            sql = "SELECT * FROM articles ORDER BY published DESC"
            rows = con.cursor().execute(sql).fetchall()
            return [Article.from_row(row) for row in rows]
