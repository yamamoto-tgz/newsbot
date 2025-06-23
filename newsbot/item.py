from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class Item:
    title: str
    link: str
    datetime: datetime
    source: str

    def time(self):
        diff = datetime.now(timezone(timedelta(hours=9))) - self.datetime
        seconds = diff.total_seconds()

        if seconds < 60:
            return "now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes}m"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h"
        elif seconds < 7 * 86400:
            days = int(seconds // 86400)
            return f"{days}d"
        else:
            return "ERROR"
