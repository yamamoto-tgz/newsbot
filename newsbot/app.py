from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template

from newsbot.gigazine import Gigazine
from newsbot.hatena import Hatena
from newsbot.nhk import Nhk

gigazine = Gigazine()
hatena = Hatena()
nhk = Nhk()


# Cron job
def job():
    gigazine.download()
    hatena.download()
    nhk.download()


scheduler = BackgroundScheduler()
scheduler.add_job(job, "cron", minute=0)  # Every hour
scheduler.start()


# Web app
app = Flask(__name__)


@app.route("/")
def index():
    gigazine_items = gigazine.items()
    hatena_items = hatena.items()
    nhk_items = nhk.items()

    all_items = gigazine_items + hatena_items + nhk_items
    all_items.sort(key=lambda item: item.datetime, reverse=True)

    return render_template(
        "index.html",
        items=all_items,
        gigazine_len=len(gigazine_items),
        hatena_len=len(hatena_items),
        nhk_len=len(nhk_items),
    )
