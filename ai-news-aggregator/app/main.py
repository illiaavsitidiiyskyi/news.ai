from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends
from app.routes import articles, sources

from app.core.database import engine, Base, get_db

# 👇 ВАЖНО: импорт моделей
from app.models import Article, Source

app = FastAPI(title="AI News Aggregator 🚀")

# 🔥 создаём таблицы при запуске
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# Роуты
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])
def read_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()


@app.get("/")
def read_root():
    return {"message": "AI News Aggregator is running!"}