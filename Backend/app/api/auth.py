

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.user import UserOut, UserCreate, Token
from sqlalchemy.orm import Session
from app.db.session import get_db
import app.repository.user_repo as user_repo 
from app.services.auth_services import get_password_hash, create_access, verify_password
from app.core.config import settings

from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

router = APIRouter()


@router.post("/signup", response_model=UserOut)
def signup(user_data:UserCreate, db:Session=Depends(get_db)):
    db_user = user_repo.get_user_by_name(db, username=user_data.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user_email = user_repo.get_user_by_email(db, email=user_data.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_repo.create_user(db, user_data)


@router.post("/login", response_model=Token)
def login(form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = user_repo.get_user_by_name(db, username= form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"www-Authenticate" : "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access(
        data={"sub":user.username}, expire_delta=access_token_expires
    )

    return {"access_token":access_token, "token_type":"bearer"}