import sqlite3
from datetime import datetime, timezone

import dateutil.parser as dateparser

DATABASE = "newsbot.db"


class Article:
    def __init__(self, id=None, channel=None, title=None, link=None, published=None, created=None, read=None):
        self.id: int = id
        self.channel: str = channel
        self.title: str = title
        self.link: str = link
        self.published: datetime = published
        self.created: datetime = created
        self.read: bool = read

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

    def save(self):
        sql = """
            UPDATE articles
            SET channel = ?, title = ?, link = ?, published = ?, created = ?, read = ?
            WHERE id = ?
        """
        values = (
            self.channel,
            self.title,
            self.link,
            self.published,
            self.created,
            self.read,
            self.id,
        )

        with sqlite3.connect(DATABASE) as con:
            con.execute(sql, values)

    @staticmethod
    def from_row(row):
        return Article(*row)

    @staticmethod
    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                channel TEXT, 
                title TEXT, 
                link TEXT, 
                published TIMESTAMP, 
                created TIMESTAMP, 
                read BOOLEAN, 
                UNIQUE (channel, title, link)
            )
        """
        with sqlite3.connect(DATABASE) as con:
            cursor = con.cursor()
            cursor.execute(sql)

    @staticmethod
    def bulk_insert(articles):
        sql = """
            INSERT INTO articles (channel, title, link, published, created, read) 
                VALUES (?, ?, ?, datetime(?), datetime(?), ?) 
                ON CONFLICT DO NOTHING
        """
        values = [[v for k, v in article.__dict__.items() if k != "id"] for article in articles]

        with sqlite3.connect(DATABASE) as con:
            rowcount = con.cursor().executemany(sql, values).rowcount
            return rowcount

    @staticmethod
    def delete_older_than(dt: datetime):
        with sqlite3.connect(DATABASE) as con:
            sql = f"DELETE FROM articles WHERE created < datetime(?)"
            rowcount = con.cursor().execute(sql, [dt]).rowcount
            return rowcount

    @staticmethod
    def find_by_id(id):
        with sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            sql = "SELECT * FROM articles WHERE id = ?"
            row = con.cursor().execute(sql, [id]).fetchone()
            return Article.from_row(row)

    @staticmethod
    def find_all_order_by_read_asc_published_desc():
        with sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES) as con:
            sql = "SELECT * FROM articles ORDER BY read ASC, published DESC"
            rows = con.cursor().execute(sql).fetchall()
            return [Article.from_row(row) for row in rows]
