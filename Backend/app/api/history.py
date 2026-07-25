
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session


from app.schemas.history import HistoryOut
from app.model.user_model import User
from app.services.auth_services import get_current_user
import app.repository.history_repo as history_repo
from app.db.session import get_db



router = APIRouter()

@router.get("/", response_model=List[HistoryOut])
def get_user_history(skip:int = 0, limit:int = 100, db:Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    histories = history_repo.get_user_history(db, user_id=current_user.id, skip = skip, limit = limit)
    return histories