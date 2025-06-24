from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, render_template

from newsbot.models.rss import Rss

load_dotenv(dotenv_path="newsbot.env")

rss_list = [
    Rss("nhk", "https://www.nhk.or.jp/rss/news/cat0.xml", "./xml/nhk.xml", "2.0"),
    Rss("atmarkit", "https://rss.itmedia.co.jp/rss/2.0/ait.xml", "./xml/atmarkit.xml", "2.0"),
    Rss("codezine", "https://codezine.jp/rss/new/20/index.xml", "./xml/codezine.xml", "2.0"),
    Rss("gizmodo", "https://www.gizmodo.jp/index.xml", "./xml/gizmodo.xml", "2.0"),
    Rss("itmedia", "https://rss.itmedia.co.jp/rss/2.0/itmedia_all.xml", "./xml/itmedia.xml", "2.0"),
    Rss("zenn", "https://zenn.dev/feed", "./xml/zenn.xml", "2.0"),
    Rss("lifehacker", "https://www.lifehacker.jp/feed/", "./xml/lifehacker.xml", "2.0"),
    Rss("gigazine", "https://gigazine.net/news/rss_2.0/", "./xml/gigazine.xml", "2.0"),
    Rss("hatena", "https://b.hatena.ne.jp/hotentry/it.rss", "./xml/hatena.xml", "1.0"),
]


# Cron job
def job():
    for rss in rss_list:
        rss.download()


scheduler = BackgroundScheduler()
scheduler.add_job(job, "cron", minute=0)
scheduler.start()


# Web app
app = Flask(__name__)


@app.route("/")
def index():
    items = [item for rss in rss_list for item in rss.items()]
    items.sort(key=lambda item: item.published, reverse=True)

    counter = dict([(rss.name, 0) for rss in rss_list])
    for item in items:
        print(f"{item.source}, {item.published}")
        counter[item.source] += 1

    return render_template("index.html", items=items, counter=counter)
