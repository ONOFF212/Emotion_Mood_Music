
import uuid
import base64
import os

from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends


from app.services.emotion_service import detect_emotion
from app.services.music_service import search_music_by_emotion
from app.services.auth_services import get_current_user
from app.schemas.history import HistoryCreate, HistoryOut, EmotionResponse
import app.repository.history_repo as history_repo
from app.model.user_model import User
from sqlalchemy.orm import Session
from app.db.session import get_db

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'Image_Folder')
os.makedirs(UPLOAD_DIR, exist_ok=True)

class base64ImageRequest(BaseModel):
    img:str
    language:str

@router.post("/detect/base64", response_model=EmotionResponse)
async def detect_emotion_base64(request:base64ImageRequest, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):

    if "," in request.img:
        header, encoded = request.img.split(",", 1)
    else:
        encoded = request.img

    str_to_img = base64.b64decode(encoded)

    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(str_to_img)

    detected_emotion = detect_emotion(filepath)
    user_language = request.language

    music_recommendation = search_music_by_emotion(detected_emotion, user_language)

    if not music_recommendation["videos"]:
        raise HTTPException(
            status_code=404,
            detail="No songs found"
        )

    first_song = music_recommendation["videos"][0]

    image_url = f"/Image_Folder/{filename}"
    history_create = HistoryCreate(
        emotion = detected_emotion,
        yt_title=first_song['title'],
        yt_video_id=first_song['video_id'],
        yt_embed_url=first_song['embed_url'],
        image_path=image_url
    )

    

    history_record = history_repo.create_history_record(db, history=history_create, user_id = current_user.id)
    return {
        "emotion": detected_emotion,
        "videos": music_recommendation["videos"],
        "history": history_record
    }


