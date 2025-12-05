@echo off
REM QNA Quiz Management System - Run Script (Windows)

echo ==========================================
echo QNA Quiz Management System
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist venv (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Check if database exists
if not exist qna.db (
    echo Warning: Database not found!
    echo Running database migration...
    python migrate_database.py
    echo.
)

REM Set Flask environment variables (optional)
set FLASK_APP=run.py
set FLASK_ENV=development

echo Starting QNA Quiz Management System...
echo.
echo Access the application at: http://127.0.0.1:5000
echo Admin login: quizmaster / 123
echo.
echo Press Ctrl+C to stop the server
echo ==========================================
echo.

REM Run the application
python run.py

pause
