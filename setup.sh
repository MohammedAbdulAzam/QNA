#!/bin/bash

# QNA Quiz Management System - Setup Script (Linux/Mac)
# This script sets up the application with a virtual environment

echo "=========================================="
echo "QNA Quiz Management System - Setup"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing old one..."
    rm -rf venv
fi

python3 -m venv venv
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ pip upgraded"
echo ""

# Install dependencies
echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "Error: requirements.txt not found"
    exit 1
fi
echo ""

# Setup database
echo "Setting up database..."
if [ -f "qna.db" ]; then
    echo "Existing database found. Creating backup..."
    cp qna.db qna.db.backup.$(date +%Y%m%d_%H%M%S)
    echo "✓ Database backed up"
    echo ""
    read -p "Do you want to delete the existing database and start fresh? (y/N): " response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        rm qna.db
        echo "✓ Old database removed"
    fi
fi

echo "Initializing database with new schema..."
python migrate_database.py
echo "✓ Database initialized"
echo ""

echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the application:"
echo "  ./run.sh"
echo ""
echo "Or manually:"
echo "  source venv/bin/activate"
echo "  python run.py"
echo ""
echo "Default admin credentials:"
echo "  Username: quizmaster"
echo "  Password: 123"
echo ""
