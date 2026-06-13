#!/bin/bash

# Create JARVIS.app - A native Mac application that can be double-clicked

APP_NAME="JARVIS"
APP_DIR="$APP_NAME.app"
CONTENTS_DIR="$APP_DIR/Contents"
MAC_OS_DIR="$CONTENTS_DIR/MacOS"
RESOURCES_DIR="$CONTENTS_DIR/Resources"

echo "🔨 Creating $APP_NAME.app..."

# Create directory structure
mkdir -p "$MAC_OS_DIR"
mkdir -p "$RESOURCES_DIR"

# Create the launcher script
cat > "$MAC_OS_DIR/$APP_NAME" << 'EOF'
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../../.." && pwd )"
cd "$DIR"

# Setup
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# Install dependencies if needed
if ! python3 -c "import pyaudio" 2>/dev/null; then
    pip install -q -r requirements-mac.txt
fi

# Run JARVIS GUI
python3 jarvis_gui.py
deactivate
EOF

chmod +x "$MAC_OS_DIR/$APP_NAME"

# Create Info.plist
cat > "$CONTENTS_DIR/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>JARVIS</string>
    <key>CFBundleIdentifier</key>
    <string>com.jarvis.voiceai</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>JARVIS</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSHumanReadableCopyright</key>
    <string>JARVIS Voice AI Assistant</string>
</dict>
</plist>
EOF

echo "✅ Created $APP_NAME.app successfully!"
echo ""
echo "📦 You can now:"
echo "   1. Double-click 'JARVIS.app' in Finder to run it"
echo "   2. Or drag it to your Applications folder"
echo "   3. Or use Spotlight: Cmd+Space, type 'JARVIS'"
echo ""
