# app/services/rss_parser.py

import feedparser
from sqlalchemy.orm import Session
from datetime import datetime
from app.models.article import Article
from app.models.source import Source

BBC_RSS_URL = "http://feeds.bbci.co.uk/news/world/rss.xml"

def fetch_bbc_news(db: Session):
    """Скачиваем новости BBC World RSS и сохраняем в базу."""
    feed = feedparser.parse(BBC_RSS_URL)

    # Получаем источник из БД или создаём новый
    source = db.query(Source).filter_by(name="BBC World").first()
    if not source:
        source = Source(name="BBC World")
        db.add(source)
        db.commit()
        db.refresh(source)

    new_articles = []

    for entry in feed.entries:
        # Пропускаем, если статья уже есть по url
        if db.query(Article).filter_by(url=entry.link).first():
            continue

        article = Article(
            title=entry.title,
            url=entry.link,  # <-- используем url вместо link
            content=getattr(entry, "summary", ""),
            published_at=datetime(*entry.published_parsed[:6]) if getattr(entry, "published_parsed", None) else None,
            source_id=source.id
        )
        db.add(article)
        new_articles.append(article)

    db.commit()
    return new_articles