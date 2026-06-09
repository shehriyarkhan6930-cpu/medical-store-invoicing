@echo off
REM Medical Store Invoicing System - Quick Start Batch File
REM This file helps start the application easily without command line

CLS
echo.
echo ======================================
echo Medical Store Invoicing System
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python is installed. Proceeding...
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install/update requirements
echo Installing dependencies...
pip install -q -r requirements.txt

REM Run the application
echo.
echo ======================================
echo Starting Medical Store Application...
echo ======================================
echo.
echo Open your browser and go to:
echo http://localhost:5000
echo.
echo Default Login:
echo Username: admin
echo Password: admin
echo.
echo Press CTRL+C to stop the application
echo.

python app/main.py

pause
