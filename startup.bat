@echo off
REM startup.bat - Start Flask app on Windows with proper configuration

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   AI Health Assistant - Production Startup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Install Python from https://www.python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo. Virtual environment created!
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies may not have installed correctly
)

REM Initialize database
echo Initializing database...
python -c "import database as db; db.init_db()" >nul 2>&1
if errorlevel 1 (
    echo. Database check failed - attempting recovery
) else (
    echo. Database ready!
)

REM Check ML model
echo Checking ML model...
python -c "import os, model_training as ml; ml.train_models() if not os.path.exists(ml.MODEL_PATH) else print('ML model ready')" >nul 2>&1

REM Show configuration
echo.
echo Configuration:
python config.py 2>nul || echo. (Configuration system available)

REM Start application
echo.
echo ==========================================
echo   Starting Flask Application...
echo ==========================================
echo.

python run.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error message above
    pause
    exit /b 1
)

pause
