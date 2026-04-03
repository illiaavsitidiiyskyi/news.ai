from app.core.database import SessionLocal
from app.models.source import Source

sources = [
    {"name": "BBC World", "rss_url": "http://feeds.bbci.co.uk/news/world/rss.xml"},
    {"name": "TechCrunch", "rss_url": "https://techcrunch.com/feed/"},
    {"name": "The Guardian", "rss_url": "https://www.theguardian.com/world/rss"},
    {"name": "HackerNews", "rss_url": "https://hnrss.org/frontpage"},
]

with SessionLocal() as db:
    for src in sources:
        exists = db.query(Source).filter(
            (Source.name == src["name"]) | (Source.rss_url == src["rss_url"])
        ).first()
        if not exists:
            db.add(Source(name=src["name"], rss_url=src["rss_url"]))
    db.commit()

print("Sources seeded successfully!")