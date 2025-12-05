#!/bin/bash

# QNA Quiz Management System - Run Script (Linux/Mac)

echo "=========================================="
echo "QNA Quiz Management System"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Check if database exists
if [ ! -f "qna.db" ]; then
    echo "Warning: Database not found!"
    echo "Running database migration..."
    python migrate_database.py
    echo ""
fi

# Set Flask environment variables (optional)
export FLASK_APP=run.py
export FLASK_ENV=development

echo "Starting QNA Quiz Management System..."
echo ""
echo "Access the application at: http://127.0.0.1:5000"
echo "Admin login: quizmaster / 123"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

# Run the application
python run.py
