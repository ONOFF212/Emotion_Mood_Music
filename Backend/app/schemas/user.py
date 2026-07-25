
from pydantic import BaseModel, EmailStr
from datetime import datetime

class userDetail(BaseModel):
    username:str
    email:EmailStr

class UserCreate(userDetail):
    password:str


class UserLogin(BaseModel):
    username:str
    password:str

class UserOut(userDetail):
    id:int
    created_at:datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token:str
    token_type:str

class tokenData(BaseModel):
    username:str
