# app/main.py (добавляем импорт парсера)
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app.routes import articles, sources
from app.core.database import engine, Base, get_db
from app.models import Article, Source
from app.services.rss_parser import fetch_bbc_news  # <-- импортируем наш парсер

app = FastAPI(title="AI News Aggregator 🚀")

# Создаём таблицы при запуске
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

    # 🔥 Подтягиваем новости BBC при старте
    db = next(get_db())
    new_articles = fetch_bbc_news(db)
    print(f"Добавлено {len(new_articles)} новых статей BBC")

# Роуты
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])

@app.get("/")
def read_root():
    return {"message": "AI News Aggregator is running!"}

@app.get("/all_articles")
def read_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()