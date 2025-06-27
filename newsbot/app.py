from datetime import datetime, timedelta, timezone

import dateutil.parser as dateparser
import feedparser
from flask import Flask, render_template, request

from newsbot.models import Article

# Database
Article.create_table()

# Web app
app = Flask(__name__)


@app.route("/")
def index():
    articles = Article.find_all_order_by_published_desc()

    counter = {}
    for article in articles:
        channel = article.channel
        counter[channel] = counter.get(channel, 0) + 1

    return render_template("index.html", articles=articles, counter=counter)


@app.route("/xml/<channel>", methods=["POST"])
def post_xml(channel):
    articles = []

    for entry in feedparser.parse(request.data).entries:
        article = Article(
            channel=channel,
            title=entry.title,
            link=entry.link,
            published=dateparser.parse(entry.updated),
            created=datetime.now(tz=timezone.utc),
        )

        threshold = datetime.now(timezone.utc) - timedelta(days=31)

        if article.is_newer_than(threshold):
            articles.append(article)

    inserted_rows = Article.bulk_insert(articles)
    print(f"{channel}: {inserted_rows} rows are inserted")

    deleted_rows = Article.delete_older_than((datetime.now(timezone.utc) - timedelta(hours=24)))
    print(f"{channel} {deleted_rows} rows are deleted")

    return "OK", 201
