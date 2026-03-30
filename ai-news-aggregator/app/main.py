# app/main.py
from fastapi import FastAPI
from app.routes import articles, sources  # убедись, что эти модули есть

app = FastAPI(title="AI News Aggregator 🚀")

# Роуты для API
app.include_router(articles.router, prefix="/articles", tags=["Articles"])
app.include_router(sources.router, prefix="/sources", tags=["Sources"])

# Корневой роут
@app.get("/")
def read_root():
    return {"message": "AI News Aggregator is running!"}