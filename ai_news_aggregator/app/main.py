from fastapi.responses import JSONResponse, Response
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import json
from datetime import datetime, date
from pathlib import Path

from app.routes import articles, sources, web
from app.core.database import engine, Base, get_db
from app.models import Article
from app.services.rss_parser import seed_sources, fetch_all_articles

# -----------------------------
# Инициализация FastAPI
# -----------------------------
app = FastAPI(title="AI News Aggregator 🚀")

# -----------------------------
# Пути к папкам шаблонов и статики
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# -----------------------------
# JSON Encoder для даты
# -----------------------------
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

# -----------------------------
# Роутеры
# -----------------------------
app.include_router(web.router)
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])

# -----------------------------
# Стартап
# -----------------------------
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    with next(get_db()) as db:
        seed_sources(db)
        new_articles = fetch_all_articles(db)
        print(f"Добавлено {len(new_articles)} новых статей из всех источников")

# -----------------------------
# Веб-интерфейс
# -----------------------------
@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    articles_list = db.query(Article).order_by(Article.id.desc()).limit(20).all()
    return templates.TemplateResponse("index.html", {"request": request, "articles": articles_list})

@app.get("/article/{article_id}")
def article_page(article_id: int, request: Request, db: Session = Depends(get_db)):
    article = db.query(Article).filter(Article.id == article_id).first()
    return templates.TemplateResponse("article.html", {"request": request, "article": article})

# -----------------------------
# API
# -----------------------------
@app.get("/all_articles")
def read_articles(db: Session = Depends(get_db)):
    return db.query(Article).all()

@app.get("/all_articles_pretty")
def read_articles_pretty(db: Session = Depends(get_db)):
    articles_list = [a.__dict__ for a in db.query(Article).all()]
    for a in articles_list:
        a.pop("_sa_instance_state", None)
    return Response(
        content=json.dumps(articles_list, cls=DateTimeEncoder, indent=4, ensure_ascii=False),
        media_type="application/json"
    )