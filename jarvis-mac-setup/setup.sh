#!/bin/bash

# JARVIS Auto-Setup Script for macOS and Linux

set -e

echo "🤖 J.A.R.V.I.S Installation Script"
echo "===================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
    REQUIREMENTS="requirements-mac.txt"
    PYTHON_CMD="python3.11"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
    REQUIREMENTS="requirements-linux.txt"
    PYTHON_CMD="python3"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "✅ Detected OS: $OS"
echo ""

# Check Python
if ! command -v $PYTHON_CMD &> /dev/null; then
    echo "❌ $PYTHON_CMD not found"
    echo "Please install Python 3.9+ first"
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD --version)
echo "✅ Found $PYTHON_VERSION"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv
source venv/bin/activate

echo "✅ Virtual environment created"
echo ""

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "✅ Pip upgraded"
echo ""

# Install requirements
echo "📥 Installing dependencies from $REQUIREMENTS..."
pip install -r $REQUIREMENTS

echo "✅ Dependencies installed"
echo ""

echo "🎉 Installation complete!"
echo ""
echo "To start JARVIS, run:"
echo "  source venv/bin/activate"
echo "  python jarvis.py"
echo ""
echo "Or create an alias:"
echo "  alias jarvis='source $(pwd)/venv/bin/activate && python $(pwd)/jarvis.py'"
