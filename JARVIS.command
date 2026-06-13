#!/bin/bash

# Maya Voice AI Assistant - Mac Launcher
# Just double-click this file to run Maya!

cd "$(dirname "$0")"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Setting up Maya for the first time..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if PyAudio is installed
if ! python3 -c "import pyaudio" 2>/dev/null; then
    echo "📥 Installing voice components..."
    pip install -q -r requirements-mac.txt
fi

# Launch Maya GUI
echo "🚀 Starting Maya..."
python3 jarvis_gui.py

# Cleanup
deactivate
