#!/bin/bash
# Maya AI Assistant - macOS Launcher

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to project directory
cd "$SCRIPT_DIR"

echo "🌟 Starting Maya AI Assistant..."
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
echo "🚀 Launching Maya..."
python3 jarvis_gui_futuristic.py

deactivate
