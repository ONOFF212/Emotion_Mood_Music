
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
import app.repository.user_repo as user_repo

from fastapi import Depends, HTTPException, status, exceptions
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
import jwt




pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access(data:dict, expire_delta: Optional[timedelta] =  None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encode_jwt


def get_current_user(token:str = Depends(oauth2_scheme), db:Session=Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"www-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username:str = payload.get("sub")
        if username is None:
            raise credential_exception
    except Exception as e:
        print("Jwt Erro:", e)
        raise credential_exception
    user = user_repo.get_user_by_name(db, username=username)
    if user is None:
        raise credential_exception
    return user