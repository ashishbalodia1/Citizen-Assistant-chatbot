import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("JWT_SECRET_KEY", "city_guardian_secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "city_guardian_secret")
    
    # Support SQLite default or MySQL when configured
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", 
        f"sqlite:///{BASE_DIR / 'city_guardian.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    UPLOAD_FOLDER = os.path.join(BASE_DIR, os.getenv("UPLOAD_FOLDER", "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

