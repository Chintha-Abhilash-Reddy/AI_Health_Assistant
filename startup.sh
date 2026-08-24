#!/bin/bash
# startup.sh - Start Flask app with proper configuration

set -e

echo "🏥 AI Health Assistant - Production Startup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check Python
python3 --version

# Install dependencies if needed
if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null || true

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Initialize database
echo "Initializing database..."
python3 -c "import database as db; db.init_db()" 2>/dev/null && echo "✓ Database ready" || echo "✓ Database already exists"

# Train ML model
echo "Checking ML model..."
python3 -c "import os, model_training as ml; ml.train_models() if not os.path.exists(ml.MODEL_PATH) else print('✓ ML model ready')"

# Show configuration
echo ""
echo "📋 Configuration:"
python3 config.py || true

# Start application
echo ""
echo "🚀 Starting Flask Application..."
python3 run.py
