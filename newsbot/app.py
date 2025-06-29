from datetime import datetime, timedelta, timezone

import dateutil.parser as dateparser
import feedparser
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, jsonify, render_template, request
from sqlalchemy import create_engine, desc, inspect
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import sessionmaker

from newsbot.models import Article, Base

# Database
engine = create_engine("sqlite:///newsbot.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Cron
def job():
    with Session() as session:
        threshold_date = datetime.now(timezone.utc) - timedelta(days=30)
        rowcount = session.query(Article).filter(Article.created <= threshold_date).delete()
        session.commit()
        print(f"deleted: {rowcount}")


scheduler = BackgroundScheduler()
scheduler.add_job(job, "cron", hour=9, minute=38)
scheduler.start()


# Web app
app = Flask(__name__)


@app.route("/")
def index():
    with Session() as session:
        articles = session.query(Article).order_by(Article.read).order_by(desc(Article.published))

        counter = {}
        for article in articles:
            channel = article.channel
            counter[channel] = counter.get(channel, 0) + 1

        return render_template("index.html", articles=articles, counter=counter)


@app.route("/xml/<channel>", methods=["POST"])
def post_xml(channel):
    articles = []
    threshold_date = datetime.now(timezone.utc) - timedelta(days=30)

    for entry in feedparser.parse(request.data).entries:
        article = Article(
            channel=channel,
            title=entry.title,
            link=entry.link,
            published=dateparser.parse(entry.updated).astimezone(timezone.utc),
            created=datetime.now(tz=timezone.utc),
            read=False,
        )

        if article.published >= threshold_date:
            articles.append(article)

    articles_table = inspect(Article).mapper.local_table
    values = [a.dict() for a in articles]
    stmt = insert(articles_table).values(values).on_conflict_do_nothing()

    with engine.begin() as conn:
        result = conn.execute(stmt)
        print(f"{channel}: {result.rowcount} rows added")

    return "OK", 201


@app.route("/articles/<int:id>", methods=["POST"])
def update(id):
    with Session() as session:
        article = session.query(Article).filter(Article.id == id).first()

        for k, v in request.get_json().items():
            setattr(article, k, v)

        session.commit()

        return jsonify(article.dict()), 200
