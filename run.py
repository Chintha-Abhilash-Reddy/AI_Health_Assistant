#!/usr/bin/env python3
"""
Production-Ready Flask Application Starter
Runs with proper error handling and configuration
"""

import os
import sys
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))

def setup_logging():
    """Configure logging for production"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(PROJECT_ROOT / 'app.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def check_requirements():
    """Verify all required packages are installed"""
    try:
        import flask
        import pandas
        import sklearn
        logger.info("✓ All required packages installed")
        return True
    except ImportError as e:
        logger.error(f"✗ Missing package: {e}")
        logger.error("Run: pip install -r requirements.txt")
        return False

def check_database():
    """Initialize database if needed"""
    try:
        from database import init_db
        init_db()
        logger.info("✓ Database initialized")
        return True
    except Exception as e:
        logger.error(f"✗ Database error: {e}")
        return False

def check_ml_model():
    """Train ML model if missing"""
    try:
        import model_training as ml
        if not os.path.exists(ml.MODEL_PATH):
            logger.info("⏳ Training ML model (first time only)...")
            ml.train_models()
            logger.info("✓ ML model trained")
        else:
            logger.info("✓ ML model loaded")
        return True
    except Exception as e:
        logger.error(f"✗ ML model error: {e}")
        return False

def start_app():
    """Start Flask application"""
    try:
        from app import app, get_local_ip
        
        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", 5000))
        debug = os.getenv("DEBUG", "False").lower() == "true"
        
        local_ip = get_local_ip()
        public_url = os.getenv("PUBLIC_APP_URL", "http://127.0.0.1:5000")
        api_url = os.getenv("API_BASE_URL", "http://127.0.0.1:5000")
        
        print("\n" + "="*80)
        print("🏥 AI HEALTH ASSISTANT — PRODUCTION READY")
        print("="*80)
        print(f"🚀 Server Starting...")
        print(f"   Host: {host}:{port}")
        print(f"   Debug: {debug}")
        print()
        print("📍 ACCESS POINTS:")
        print(f"   Local Machine    : http://127.0.0.1:{port}")
        print(f"   Local Network    : http://{local_ip}:{port}")
        print(f"   Public URL       : {public_url}")
        print(f"   API Base URL     : {api_url}")
        print()
        print("📱 MOBILE APPS:")
        print(f"   Android API: {api_url}")
        print(f"   iOS API:    {api_url}")
        print()
        print("="*80)
        print(f"✓ Ready at http://127.0.0.1:{port}")
        print("="*80 + "\n")
        
        app.run(host=host, port=port, debug=debug, threaded=True)
        
    except Exception as e:
        logger.error(f"✗ Failed to start app: {e}", exc_info=True)
        sys.exit(1)

def main():
    """Main entry point"""
    logger.info("🏥 AI Health Assistant - Starting Application")
    
    # Verify environment
    checks = [
        ("Dependencies", check_requirements),
        ("Database", check_database),
        ("ML Model", check_ml_model),
    ]
    
    for name, check_func in checks:
        if not check_func():
            logger.error(f"Failed at: {name}")
            sys.exit(1)
    
    # Start application
    start_app()

if __name__ == "__main__":
    main()
