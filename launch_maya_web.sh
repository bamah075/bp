#!/bin/bash
# Maya Web UI Server Launcher

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$PROJECT_DIR"

echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║       🌟 MAYA WEB UI SERVER - STARTING 🌟         ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📥 Installing Flask and dependencies..."
    pip install flask flask-cors -q
fi

# Start the web server
echo "🚀 Starting Maya Web Server..."
echo ""
echo "📱 Web Interface: http://localhost:5000"
echo "🔌 API Endpoint: http://localhost:5000/api"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 maya_web_server.py

deactivate
