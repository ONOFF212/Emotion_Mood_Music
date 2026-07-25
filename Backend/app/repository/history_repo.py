
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

def get_user_history(db:Session, user_id:int, skip:int= 0, limit:int = 100):
    return db.query(History).filter(History.user_id == user_id).order_by(History.timestamp.desc()).offset(skip).limit(limit).all()