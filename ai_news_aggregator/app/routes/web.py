from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from types import SimpleNamespace

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Временные данные как объекты с атрибутами
fake_articles = [
    SimpleNamespace(id=1, title="AI is taking over", content="Full article text..."),
    SimpleNamespace(id=2, title="Tech news today", content="Another article..."),
]

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"articles": fake_articles}
    )

@router.get("/article/{article_id}")
def article(request: Request, article_id: int):
    article_obj = next(a for a in fake_articles if a.id == article_id)
    return templates.TemplateResponse(
        request=request,
        name="article.html",
        context={"article": article_obj}
    )