from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import datetime

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)
    url = Column(String, unique=True, index=True)
    published_at = Column(DateTime, default=datetime.datetime.utcnow)
    source_id = Column(Integer, ForeignKey("sources.id"))

    source = relationship("Source", back_populates="articles")