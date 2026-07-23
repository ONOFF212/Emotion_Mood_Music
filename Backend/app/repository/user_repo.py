

from sqlalchemy.orm import Session
from app.model.user_model import User
from app.schemas.user import UserCreate
from app.services.auth_services import get_password_hash

def get_user_by_name(db:Session, username:str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db:Session, email:str):
    return db.query(User).filter(User.email == email).first()

def get_user_id(db:Session, user_id:int):
    return db.query(User).filter(User.id == user_id).first();

def create_user(db:Session, user_data:UserCreate):
    hashed_password = get_password_hash(user_data.password)
    db_user = User(
        username = user_data.username,
        email = user_data.email,
        hashed_password = hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user