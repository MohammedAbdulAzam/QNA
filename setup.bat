@echo off
REM QNA Quiz Management System - Setup Script (Windows)
REM This script sets up the application with a virtual environment

echo ==========================================
echo QNA Quiz Management System - Setup
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python found
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
echo [OK] Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo [OK] pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
if exist requirements.txt (
    pip install -r requirements.txt
    echo [OK] Dependencies installed
) else (
    echo Error: requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Setup database
echo Setting up database...
if exist qna.db (
    echo Existing database found. Creating backup...
    copy qna.db qna.db.backup.%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    echo [OK] Database backed up
    echo.
    set /p response="Do you want to delete the existing database and start fresh? (y/N): "
    if /i "%response%"=="y" (
        del qna.db
        echo [OK] Old database removed
    )
)

echo Initializing database with new schema...
python migrate_database.py
echo [OK] Database initialized
echo.

echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To start the application:
echo   run.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python run.py
echo.
echo Default admin credentials:
echo   Username: quizmaster
echo   Password: 123
echo.
pause
