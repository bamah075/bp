#!/bin/bash
# Quick launcher script for JARVIS GUI

echo "🤖 Starting JARVIS Voice AI Assistant..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Check if dependencies are installed
if ! python3 -c "import pyaudio" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements-mac.txt -q
fi

# Launch GUI
echo "🚀 Launching JARVIS GUI..."
python3 jarvis_gui.py

deactivate
