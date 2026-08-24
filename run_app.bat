@echo off
title AI Health Assistant Launcher
cd /d "%~dp0"
echo ========================================================
echo       Starting AI Health Assistant Application...
echo ========================================================
echo.
echo Launching server at http://127.0.0.1:5000/login
echo.

:: Open the browser directly to the login page after 2 seconds in the background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000/login"

:: Run the Python Flask application
python app.py

pause
