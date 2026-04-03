from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    rss_url = Column(String, unique=True, nullable=False)

    # Один источник -> много статей
    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")