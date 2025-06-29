from sqlalchemy import Boolean, Column, DateTime, Integer, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
from datetime import datetime, timezone


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    channel = Column(Text)
    title = Column(Text)
    link = Column(Text)
    published = Column(DateTime)
    created = Column(DateTime)
    read = Column(Boolean)
    __table_args__ = (UniqueConstraint("channel", "title", "link"),)

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

    def dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
