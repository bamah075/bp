#!/bin/bash

# Maya Futuristic Edition - Mac Launcher
# Full animated sci-fi experience with visual effects

cd "$(dirname "$0")"

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "🔧 Setting up Maya Futuristic for the first time..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Check if PyAudio is installed
if ! python3 -c "import pyaudio" 2>/dev/null; then
    echo "📥 Installing voice components..."
    pip install -q -r requirements-mac.txt
fi

# Launch Maya Futuristic GUI
echo "🚀 Starting Maya Futuristic..."
python3 jarvis_gui_futuristic.py

# Cleanup
deactivate
