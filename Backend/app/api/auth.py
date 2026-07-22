

from fastapi import APIRouter


router = APIRouter()


@router.post("/signup")
def signup():
    return True


@router.post("/login")
def login():
    return True