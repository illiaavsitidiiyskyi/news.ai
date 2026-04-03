# app/main.py
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime, date
from starlette.responses import Response
from app.routes import articles, sources
from app.core.database import engine, Base, get_db
from app.models import Article, Source
from app.services.rss_parser import seed_sources, fetch_all_articles

app = FastAPI(title="AI News Aggregator 🚀")

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db: Session = next(get_db())
    seed_sources(db)
    new_articles = fetch_all_articles(db)
    print(f"Добавлено {len(new_articles)} новых статей из всех источников")

app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])

@app.get("/")
def read_root():
    return {"message": "AI News Aggregator is running!"}

@app.get("/all_articles")
def read_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@app.get("/all_articles_pretty")
def read_articles_pretty(db: Session = Depends(get_db)):
    articles = db.query(Article).all()
    articles_list = [article.__dict__ for article in articles]
    for a in articles_list:
        a.pop("_sa_instance_state", None)
    return Response(
        content=json.dumps(articles_list, cls=DateTimeEncoder, indent=4, ensure_ascii=False),
        media_type="application/json"
    )