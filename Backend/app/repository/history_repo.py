
from sqlalchemy.orm import Session
from app.model.history import History
from app.schemas.history import HistoryCreate

def create_history_record(db:Session, history:HistoryCreate, user_id:int):
    db_history = History(
        user_id = user_id,
        emotion = history.emotion,
        image_path = history.image_path,
        yt_title=history.yt_title,
        yt_video_id=history.yt_video_id,
        yt_embed_url=history.yt_embed_url
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history