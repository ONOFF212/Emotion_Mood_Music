
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HistoryBase(BaseModel):
    emotion:str
    yt_title:Optional[str] = None
    yt_video_id:Optional[str] = None
    yt_embed_url:Optional[str] = None

class HistoryCreate(HistoryBase):
    image_path:Optional[str] = None

class HistoryOut(HistoryBase):
    id:int
    user_id:int
    image_path:Optional[str] = None
    timestamp:datetime

    class Config:
        from_attributes = True

class VideoRecommendation(BaseModel):
    title: str
    video_id: str
    embed_url: str


class EmotionResponse(BaseModel):
    emotion: str
    videos: List[VideoRecommendation]
    history: HistoryOut

class EmotionSummary(BaseModel):
    Happy: float = 0
    Sad: float = 0
    Angry: float = 0
    Neutral: float = 0
    Fear: float = 0
    Surprise: float = 0
    Disgust: float = 0