#!/bin/bash
# Medical Store Invoicing System - Quick Start Script for macOS/Linux

echo ""
echo "======================================"
echo "Medical Store Invoicing System"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3 from https://www.python.org/downloads/"
    exit 1
fi

echo "Python is installed. Proceeding..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Run the application
echo ""
echo "======================================"
echo "Starting Medical Store Application..."
echo "======================================"
echo ""
echo "Open your browser and go to:"
echo "http://localhost:5000"
echo ""
echo "Default Login:"
echo "Username: admin"
echo "Password: admin"
echo ""
echo "Press CTRL+C to stop the application"
echo ""

python3 app/main.py
