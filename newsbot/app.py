from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from flask import Flask, render_template

from newsbot.codezine import Codezine
from newsbot.gigazine import Gigazine
from newsbot.hatena import Hatena
from newsbot.nhk import Nhk
from newsbot.zenn import Zenn

load_dotenv(dotenv_path="newsbot.env")

rss_list = [Gigazine(), Codezine(), Hatena(), Zenn(), Nhk()]


# Cron job
def job():
    for rss in rss_list:
        rss.download()


scheduler = BackgroundScheduler()
scheduler.add_job(job, "cron", minute=0)  # Every hour
scheduler.start()


# Web app
app = Flask(__name__)


@app.route("/")
def index():
    items = [item for rss in rss_list for item in rss.items()]
    items.sort(key=lambda item: item.datetime, reverse=True)

    count = dict([(rss.name, 0) for rss in rss_list])
    for item in items:
        count[item.source] += 1

    return render_template("index.html", items=items, count=count)
