from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    emotion = Column(String(50), nullable=False)
    image_path = Column(String(255))
    yt_title = Column(String(255))
    yt_video_id = Column(String(100))
    yt_embed_url = Column(String(255))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="histories")