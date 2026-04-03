from app.services.rss_parser import fetch_all_articles, save_articles
from app.core.database import SessionLocal

def run_parser():
    db = SessionLocal()

    articles = fetch_all_articles(db)
    save_articles(db, articles)

    db.close()