from app.core.database import SessionLocal
from app.models.source import Source

with SessionLocal() as db:
    for src in db.query(Source).all():
        print(src.name, src.rss_url)