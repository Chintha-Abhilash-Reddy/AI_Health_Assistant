"""
Production Configuration System
Handles environment-specific settings for web, Android, iOS, and API deployment.
Supports SQLite (local) and PostgreSQL / MySQL (cloud) databases.
"""

import os
import secrets
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

def get_database_url():
    """Retrieve and normalize database URL (e.g. fix postgres:// for SQLAlchemy/PostgreSQL)"""
    url = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'health.db'}")
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url

class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    
    # Secret Key
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    
    # URLs - Used across mobile apps and web frontend
    PUBLIC_WEB_URL = os.getenv("PUBLIC_WEB_URL", "http://127.0.0.1:5000").rstrip("/")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
    
    # Store URLs (for download page QR codes and mobile app links)
    ANDROID_STORE_URL = os.getenv(
        "ANDROID_STORE_URL",
        "https://play.google.com/store/apps/details?id=com.health.aiassistant"
    )
    IOS_STORE_URL = os.getenv(
        "IOS_STORE_URL",
        "https://apps.apple.com/app/ai-health-assistant/id6739271845"
    )
    
    # Email Configuration
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
    EMAIL_DEV_MODE = os.getenv("EMAIL_DEV_MODE", "true").lower() == "true"
    
    # CORS for Mobile Apps and Web Frontends
    ALLOWED_ORIGINS = [
        o.strip() for o in os.getenv(
            "ALLOWED_ORIGINS",
            "*,http://localhost:5000,http://127.0.0.1:5000,capacitor://localhost,ionic://localhost"
        ).split(",") if o.strip()
    ]
    
    # Database
    DATABASE_URL = get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security & File Uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads", "reports")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False
    PUBLIC_WEB_URL = os.getenv("PUBLIC_WEB_URL", "http://127.0.0.1:5000").rstrip("/")
    API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:5000").rstrip("/")

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    
    # Enforce HTTPS session cookies when in full production
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "true").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    
    PUBLIC_WEB_URL = os.getenv("PUBLIC_WEB_URL", "https://app.example.com").rstrip("/")
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com").rstrip("/")
    
    ANDROID_STORE_URL = os.getenv(
        "ANDROID_STORE_URL",
        "https://play.google.com/store/apps/details?id=com.health.aiassistant"
    )
    IOS_STORE_URL = os.getenv(
        "IOS_STORE_URL",
        "https://apps.apple.com/app/ai-health-assistant/id6739271845"
    )

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = False

def get_config():
    """Get configuration based on FLASK_ENV or ENVIRONMENT variable"""
    env = (os.getenv("FLASK_ENV") or os.getenv("ENVIRONMENT") or "development").lower()
    
    configs = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "prod": ProductionConfig,
        "testing": TestingConfig,
        "test": TestingConfig,
    }
    
    return configs.get(env, DevelopmentConfig)

def print_config():
    """Debug: Print current configuration summary"""
    config = get_config()
    print("\n" + "="*70)
    print(f"CURRENT CONFIGURATION ({config.__name__})")
    print("="*70)
    for key, value in vars(config).items():
        if not key.startswith("_"):
            if any(k in key for k in ["PASSWORD", "SECRET", "KEY", "TOKEN"]):
                value = "***HIDDEN***"
            print(f"{key:.<40} {value}")
    print("="*70 + "\n")

