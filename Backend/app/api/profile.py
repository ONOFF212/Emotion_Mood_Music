
from fastapi import APIRouter, Depends
from app.model.user_model import User
from app.schemas.user import UserOut
from app.services.auth_services import get_current_user
from app.schemas.history import EmotionSummary

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.session import get_db
from app.model.history import History

router = APIRouter()

@router.get("/", response_model=UserOut)
def read_user(current_user:User = Depends(get_current_user)):
    return current_user



@router.get("/emotion-summary", response_model=EmotionSummary)
def emotion_summary(
    db:Session = Depends(get_db), current_user : User=Depends(get_current_user)
):
    histories = (db.query(History).filter(History.user_id == current_user.id).all())

    emotion_counts = {}
    for history in histories:
        emotion = history.emotion
        if emotion not in emotion_counts:
            emotion_counts[emotion] = 0
        emotion_counts[emotion] += 1

    total = len(histories)
    emotion_percentages = {
        "Happy": 0,
        "Sad": 0,
        "Angry": 0,
        "Neutral": 0,
        "Fear": 0,
        "Surprise": 0,
        "Disgust": 0,
    }
    if total == 0:
        return emotion_percentages
    
    for emotion, count in emotion_counts.items():
        emotion = emotion.capitalize()
        emotion_percentages[emotion] = round((count / total) * 100, 2)

    return emotion_percentages