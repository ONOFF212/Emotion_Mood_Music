
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from app.api import auth , emotion , profile

app = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
FRONTEND_DIR = BASE_DIR / "Frontend"


app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(emotion.router, prefix="/api/emotion", tags=["emotion"])
app.include_router(profile.router, prefix="/api/profile", tags=["profile"])


app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="Frontend")


@app.get("/")
def root():
    return{"message": "Hello,World"}


