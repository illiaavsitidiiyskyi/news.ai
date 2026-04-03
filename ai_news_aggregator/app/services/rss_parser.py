# app/services/rss_parser.py

import feedparser
from sqlalchemy.orm import Session
from datetime import datetime
import hashlib
from app.models.article import Article
from app.models.source import Source

# Список источников (можно расширять)
DEFAULT_SOURCES = [
    {"name": "BBC World", "rss_url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "TechCrunch", "rss_url": "https://techcrunch.com/feed/"},
    {"name": "The Guardian", "rss_url": "https://www.theguardian.com/world/rss"},
    {"name": "HackerNews", "rss_url": "https://hnrss.org/frontpage"},
]

def make_hash(article_data):
    """Создаём хеш для статьи по title+content."""
    raw = (article_data["title"] + article_data["content"]).strip()
    return hashlib.md5(raw.encode("utf-8")).hexdigest()

def seed_sources(db: Session):
    """Добавляем источники в БД, если их ещё нет."""
    for src in DEFAULT_SOURCES:
        # проверяем сразу по имени и rss_url
        exists = db.query(Source).filter(
            (Source.name == src["name"]) | (Source.rss_url == src["rss_url"])
        ).first()
        if not exists:
            db.add(Source(name=src["name"], rss_url=src["rss_url"]))
    db.commit()

def fetch_all_articles(db: Session):
    """Скачиваем новости со всех источников."""
    sources = db.query(Source).all()
    all_articles = []
    seen_urls = set()  # отслеживаем URL в памяти

    for source in sources:
        if not source.rss_url:
            print(f"Пропуск источника {source.name!r}: rss_url пустой")
            continue
        feed = feedparser.parse(source.rss_url)
        for entry in feed.entries:
            url = entry.link

            # Пропускаем дубликаты: в БД и в текущем батче
            if url in seen_urls or db.query(Article).filter(Article.url == url).first():
                continue

            seen_urls.add(url)

            article_data = {
                "title": entry.title,
                "url": url,
                "content": getattr(entry, "summary", getattr(entry, "description", "")),
                "published_at": datetime(*entry.published_parsed[:6]) if getattr(entry, "published_parsed", None) else None,
                "source_id": source.id
            }

            content_hash = make_hash(article_data)
            article = Article(**article_data, content_hash=content_hash)
            db.add(article)
            all_articles.append(article)

    db.commit()
    return all_articles